import socket
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db_query_protocol import decode_message, encode_message, receive_message, send_request


class ProtocolTest(unittest.TestCase):
    def test_round_trip_over_a_unix_socket(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            socket_path = str(Path(temporary_directory) / "broker.sock")
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            server.bind(socket_path)
            server.listen(1)

            def serve_once() -> None:
                connection, _ = server.accept()
                with connection:
                    request = receive_message(connection)
                    self.assertEqual(request, {"operation": "list"})
                    connection.sendall(encode_message({"ok": True, "result": {"databases": []}}))

            thread = threading.Thread(target=serve_once)
            thread.start()
            self.assertEqual(send_request(socket_path, {"operation": "list"}), {"ok": True, "result": {"databases": []}})
            thread.join()
            server.close()

    def test_rejects_invalid_json(self) -> None:
        with self.assertRaisesRegex(ValueError, "mensagem_invalida"):
            decode_message(b"not-json")
