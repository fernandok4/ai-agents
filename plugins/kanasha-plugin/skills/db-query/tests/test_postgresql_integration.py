import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db_query_protocol import send_request


SOCKET_PATH = os.environ.get("DB_QUERY_INTEGRATION_SOCKET")
DATABASE_ALIAS = os.environ.get("DB_QUERY_INTEGRATION_ALIAS")
RELATION = os.environ.get("DB_QUERY_INTEGRATION_RELATION")


@unittest.skipUnless(
    SOCKET_PATH and DATABASE_ALIAS and RELATION,
    "requer fixture PostgreSQL isolada declarada por DB_QUERY_INTEGRATION_SOCKET, DB_QUERY_INTEGRATION_ALIAS e DB_QUERY_INTEGRATION_RELATION",
)
class PostgreSqlIntegrationTest(unittest.TestCase):
    def test_authorized_select_uses_the_broker(self) -> None:
        response = send_request(
            SOCKET_PATH,
            {
                "operation": "query",
                "db": DATABASE_ALIAS,
                "sql": f"SELECT id FROM {RELATION} LIMIT 1",
                "params": [],
            },
        )

        self.assertTrue(response["ok"], response)
