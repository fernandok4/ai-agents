import grp
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

import yaml


SKILL_DIRECTORY = Path(__file__).resolve().parents[1]


def config_document(alias: str) -> dict[str, object]:
    return {
        "databases": {
            alias: {
                "enabled": True,
                "type": "postgresql",
                "host": "postgres.example.invalid",
                "port": 5432,
                "database": "example_database",
                "username": "reader",
                "password": "not-a-real-secret",
                "allowed_schemas": ["public"],
                "allowed_relations": ["public.example_safe_view"],
            }
        }
    }


class BrokerListTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.config_path = Path(self.temporary_directory.name) / "databases.yaml"
        self.socket_path = Path(self.temporary_directory.name) / "broker.sock"
        self.write_config(config_document("first_alias"))
        socket_group = grp.getgrgid(os.getgid()).gr_name
        environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        self.broker = subprocess.Popen(
            [
                sys.executable,
                str(SKILL_DIRECTORY / "db_query_broker.py"),
                "--config",
                str(self.config_path),
                "--socket",
                str(self.socket_path),
                "--socket-group",
                socket_group,
            ],
            cwd=SKILL_DIRECTORY,
            env=environment,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.wait_for_socket()

    def tearDown(self) -> None:
        if self.broker.poll() is None:
            self.broker.terminate()
            self.broker.wait(timeout=5)
        self.broker.stderr.close()
        self.temporary_directory.cleanup()

    def write_config(self, document: dict[str, object]) -> None:
        self.config_path.write_text(yaml.safe_dump(document), encoding="utf-8")

    def wait_for_socket(self) -> None:
        for _ in range(100):
            if self.socket_path.exists():
                return
            if self.broker.poll() is not None:
                details = self.broker.stderr.read()
                self.fail(f"broker não iniciou: {details}")
            time.sleep(0.01)
        self.fail("broker não criou o socket")

    def list_aliases(self) -> list[str]:
        client = subprocess.run(
            [
                sys.executable,
                str(SKILL_DIRECTORY / "db_query.py"),
                "--socket",
                str(self.socket_path),
                "list",
                "--format",
                "json",
            ],
            cwd=SKILL_DIRECTORY,
            capture_output=True,
            check=True,
            text=True,
        )
        response = json.loads(client.stdout)
        return [database["alias"] for database in response["databases"]]

    def test_client_lists_aliases_and_invalid_reload_keeps_the_previous_configuration(self) -> None:
        self.assertEqual(self.list_aliases(), ["first_alias"])

        self.config_path.write_text("databases: invalid", encoding="utf-8")
        self.broker.send_signal(signal.SIGHUP)
        time.sleep(0.05)

        self.assertEqual(self.list_aliases(), ["first_alias"])
