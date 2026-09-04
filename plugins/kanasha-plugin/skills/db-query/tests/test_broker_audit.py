import asyncio
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db_query_broker import process_request


DATABASES = {
    "example_postgres": {
        "host": "db.private.invalid",
        "password": "not-a-real-secret",
        "allowed_relations": ["public.example_safe_view"],
        "allowed_functions": [],
        "max_rows": 100,
    }
}


class BrokerAuditTest(unittest.TestCase):
    def test_authorized_query_log_excludes_connection_and_parameter_values(self) -> None:
        request = {
            "operation": "query",
            "db": "example_postgres",
            "sql": "SELECT id FROM public.example_safe_view WHERE application_id = $1 LIMIT 10",
            "params": ["sensitive-parameter@example.invalid"],
        }
        result = {"columns": ["id"], "rows": [["result-that-must-not-be-logged"]], "row_count": 1}

        with patch("db_query_broker.execute_query", new_callable=AsyncMock, return_value=result):
            with self.assertLogs(level="INFO") as logs:
                response = asyncio.run(process_request(request, DATABASES, uid=1234))

        self.assertEqual(response, result)
        emitted_logs = "\n".join(logs.output)
        for forbidden_value in (
            "db.private.invalid",
            "not-a-real-secret",
            "sensitive-parameter@example.invalid",
            "result-that-must-not-be-logged",
        ):
            self.assertNotIn(forbidden_value, emitted_logs)
