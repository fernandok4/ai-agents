#!/usr/bin/env python3
"""Broker PostgreSQL read-only que mantém credenciais fora do processo cliente."""

import argparse
import asyncio
import grp
import logging
import os
import signal
import socket
import stat
import struct
import time
from pathlib import Path

from db_query_config import get_database, get_relation, load_config, public_databases
from db_query_postgresql import describe_relation, execute_query
from db_query_protocol import read_message, write_message
from db_query_validator import validate_query


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Broker local PostgreSQL read-only")
    parser.add_argument("--config", required=True, help="Arquivo YAML privado, lido apenas pelo broker.")
    parser.add_argument("--socket", required=True, help="Socket Unix local criado pelo broker.")
    parser.add_argument("--socket-group", required=True, help="Grupo Unix autorizado a usar o socket.")
    parser.add_argument("--validate-config", action="store_true", help="Valida somente a sintaxe e a política do YAML.")
    return parser


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def remove_stale_socket(socket_path: Path) -> None:
    if not socket_path.exists():
        return
    socket_status = socket_path.lstat()
    if not stat.S_ISSOCK(socket_status.st_mode) or socket_status.st_uid != os.geteuid():
        raise RuntimeError("socket_indisponivel")
    socket_path.unlink()


def set_socket_permissions(socket_path: Path, group_name: str) -> None:
    group_id = grp.getgrnam(group_name).gr_gid
    os.chown(socket_path, -1, group_id)
    os.chmod(socket_path, 0o660)


def peer_uid(writer: asyncio.StreamWriter) -> int | None:
    connection = writer.get_extra_info("socket")
    if connection is None or not hasattr(socket, "SO_PEERCRED"):
        return None
    try:
        credentials = connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i"))
        _, uid, _ = struct.unpack("3i", credentials)
        return uid
    except OSError:
        return None


def audit(event: str, uid: int | None, alias: object = "-", **fields: object) -> None:
    details = " ".join(f"{key}={value}" for key, value in fields.items())
    logging.info("event=%s uid=%s alias=%s %s", event, uid if uid is not None else "unknown", alias, details)


async def process_request(request: dict[str, object], databases: dict[str, dict[str, object]], uid: int | None) -> dict[str, object]:
    operation = request.get("operation")
    if operation == "list":
        audit("list", uid)
        return {"databases": public_databases(databases)}

    database = get_database(databases, request.get("db"))
    alias = request.get("db")
    started_at = time.monotonic()
    if operation == "describe":
        schema, relation = get_relation(database, request.get("relation"))
        result = await describe_relation(database, schema, relation)
        audit("describe", uid, alias, relation=f"{schema}.{relation}", rows=result["row_count"], duration_ms=duration_ms(started_at))
        return result

    if operation == "query":
        validated = validate_query(request.get("sql"), request.get("params"), database)
        result = await execute_query(database, str(validated["sql"]), request["params"])
        audit("query", uid, alias, query=validated["audit_summary"], rows=result["row_count"], duration_ms=duration_ms(started_at))
        return result

    raise ValueError("operacao_nao_autorizada")


def duration_ms(started_at: float) -> int:
    return int((time.monotonic() - started_at) * 1_000)


async def serve(config_path: str, socket_path: Path, socket_group: str) -> None:
    state = {"databases": load_config(config_path)}
    remove_stale_socket(socket_path)

    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        uid = peer_uid(writer)
        try:
            request = await read_message(reader)
            result = await process_request(request, state["databases"], uid)
            await write_message(writer, {"ok": True, "result": result})
        except ValueError as error:
            audit("request_rejected", uid, code=str(error))
            await write_message(writer, {"ok": False, "error": {"code": str(error)}})
        except Exception:
            audit("database_query_failed", uid)
            await write_message(writer, {"ok": False, "error": {"code": "consulta_indisponivel"}})
        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_unix_server(handle_client, path=str(socket_path))
    set_socket_permissions(socket_path, socket_group)
    logging.info("event=broker_started configured_databases=%s", len(state["databases"]))

    def reload_config() -> None:
        try:
            state["databases"] = load_config(config_path)
        except ValueError:
            logging.error("event=config_reload_rejected")
        else:
            logging.info("event=config_reloaded configured_databases=%s", len(state["databases"]))

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGHUP, reload_config)
    try:
        async with server:
            await server.serve_forever()
    finally:
        socket_path.unlink(missing_ok=True)


def main() -> int:
    configure_logging()
    args = build_parser().parse_args()
    if args.validate_config:
        databases = load_config(args.config)
        print(f"configuracao_valida aliases={len(databases)}")
        return 0
    try:
        asyncio.run(serve(args.config, Path(args.socket), args.socket_group))
    except (OSError, RuntimeError, ValueError):
        logging.error("event=broker_start_failed")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
