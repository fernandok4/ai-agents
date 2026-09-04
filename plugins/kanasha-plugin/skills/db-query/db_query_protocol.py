"""Protocolo JSON delimitado por linha para o socket Unix do broker."""

import json
import socket


MAX_MESSAGE_BYTES = 64 * 1024


def encode_message(payload: dict[str, object]) -> bytes:
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"), default=str).encode("utf-8")
    if len(encoded) > MAX_MESSAGE_BYTES:
        raise ValueError("mensagem_excede_limite")
    return encoded + b"\n"


def decode_message(payload: bytes) -> dict[str, object]:
    if not payload or len(payload) > MAX_MESSAGE_BYTES:
        raise ValueError("mensagem_invalida")
    try:
        decoded = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("mensagem_invalida") from error
    if not isinstance(decoded, dict):
        raise ValueError("mensagem_invalida")
    return decoded


def receive_message(connection: socket.socket) -> dict[str, object]:
    chunks: list[bytes] = []
    received = 0
    while True:
        chunk = connection.recv(4096)
        if not chunk:
            break
        received += len(chunk)
        if received > MAX_MESSAGE_BYTES + 1:
            raise ValueError("mensagem_excede_limite")
        chunks.append(chunk)
        if b"\n" in chunk:
            break

    payload = b"".join(chunks)
    line, separator, remainder = payload.partition(b"\n")
    if not separator or remainder:
        raise ValueError("mensagem_invalida")
    return decode_message(line)


def send_request(socket_path: str, request: dict[str, object]) -> dict[str, object]:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(15)
        connection.connect(socket_path)
        connection.sendall(encode_message(request))
        return receive_message(connection)


async def read_message(reader: object) -> dict[str, object]:
    line = await reader.readline()
    return decode_message(line.rstrip(b"\n"))


async def write_message(writer: object, payload: dict[str, object]) -> None:
    writer.write(encode_message(payload))
    await writer.drain()
