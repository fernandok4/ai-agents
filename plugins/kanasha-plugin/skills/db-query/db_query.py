#!/usr/bin/env python3
"""Cliente sem credenciais para o broker local de consultas."""

import argparse
import csv
import io
import json
import os
import sys

from db_query_protocol import send_request


def format_table(columns: list[str], rows: list[list[object]]) -> str:
    if not columns:
        return "(sem resultados)"

    text_rows = [
        ["NULL" if value is None else str(value) for value in row]
        for row in rows
    ]
    widths = [len(column) for column in columns]
    for row in text_rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    header = " | ".join(column.ljust(width) for column, width in zip(columns, widths))
    separator = "-+-".join("-" * width for width in widths)
    body = [" | ".join(value.ljust(width) for value, width in zip(row, widths)) for row in text_rows]
    return "\n".join([header, separator, *body])


def format_csv(columns: list[str], rows: list[list[object]]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(columns)
    writer.writerows(rows)
    return buffer.getvalue().rstrip()


def print_result(response: dict[str, object], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(response, ensure_ascii=False, indent=2, default=str))
        return

    if "databases" in response:
        databases = response["databases"]
        rows = [
            [database["alias"], database["type"], database.get("description", "")]
            for database in databases
        ]
        columns = ["alias", "type", "description"]
    else:
        columns = response.get("columns", [])
        rows = response.get("rows", [])

    if output_format == "csv":
        print(format_csv(columns, rows))
        return

    print(format_table(columns, rows))
    if "row_count" in response:
        print(f"\n({response['row_count']} linhas retornadas)")


def parse_params(raw_params: str) -> list[object]:
    try:
        params = json.loads(raw_params)
    except json.JSONDecodeError as error:
        raise ValueError("params_invalidos") from error
    if not isinstance(params, list):
        raise ValueError("params_devem_ser_uma_lista_json")
    return params


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cliente do broker PostgreSQL read-only")
    parser.add_argument(
        "--socket",
        default=os.environ.get("DB_QUERY_SOCKET"),
        help="Caminho do socket Unix definido pela instalação local.",
    )
    subparsers = parser.add_subparsers(dest="operation", required=True)

    list_parser = subparsers.add_parser("list", help="Lista aliases disponíveis sem revelar conexões.")
    list_parser.add_argument("--format", choices=("table", "json", "csv"), default="table")

    describe_parser = subparsers.add_parser("describe", help="Descreve uma relação autorizada.")
    describe_parser.add_argument("--db", required=True)
    describe_parser.add_argument("--relation", required=True)
    describe_parser.add_argument("--format", choices=("table", "json", "csv"), default="table")

    query_parser = subparsers.add_parser("query", help="Executa uma SELECT parametrizada autorizada.")
    query_parser.add_argument("--db", required=True)
    query_parser.add_argument("--sql", required=True)
    query_parser.add_argument("--params", default="[]", help="Lista JSON para placeholders PostgreSQL $1, $2, ...")
    query_parser.add_argument("--format", choices=("table", "json", "csv"), default="table")
    return parser


def build_request(args: argparse.Namespace) -> dict[str, object]:
    if args.operation == "list":
        return {"operation": "list"}
    if args.operation == "describe":
        return {"operation": "describe", "db": args.db, "relation": args.relation}
    return {
        "operation": "query",
        "db": args.db,
        "sql": args.sql,
        "params": parse_params(args.params),
    }


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not args.socket:
        parser.error("informe --socket ou defina DB_QUERY_SOCKET")

    try:
        response = send_request(args.socket, build_request(args))
    except (OSError, ValueError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1

    if not response.get("ok"):
        error = response.get("error", {})
        print(f"Erro: {error.get('code', 'broker_indisponivel')}", file=sys.stderr)
        return 1

    print_result(response["result"], args.format)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
