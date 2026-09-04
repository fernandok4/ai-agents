import asyncio
import sys
import unittest
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db_query_postgresql import execute_query, fetch_read_only


DATABASE = {
    "host": "postgres.example.invalid",
    "port": 5432,
    "database": "example_database",
    "username": "reader",
    "password": "not-a-real-secret",
    "connect_timeout_seconds": 5,
    "statement_timeout_ms": 10000,
    "max_rows": 100,
}


class PostgresqlTest(unittest.TestCase):
    def test_executes_in_a_read_only_transaction_with_a_statement_timeout(self) -> None:
        transaction_options: list[dict[str, object]] = []

        @asynccontextmanager
        async def transaction(**kwargs: object):
            transaction_options.append(kwargs)
            yield

        statement = SimpleNamespace(
            fetch=AsyncMock(return_value=[SimpleNamespace(values=lambda: ["value"]) ]),
            get_attributes=lambda: [SimpleNamespace(name="id")],
        )
        connection = SimpleNamespace(
            transaction=transaction,
            execute=AsyncMock(),
            prepare=AsyncMock(return_value=statement),
            close=AsyncMock(),
        )
        asyncpg = SimpleNamespace(connect=AsyncMock(return_value=connection))

        with patch.dict(sys.modules, {"asyncpg": asyncpg}):
            result = asyncio.run(fetch_read_only(DATABASE, "SELECT id FROM public.example_safe_view LIMIT 1", []))

        self.assertEqual(result, {"columns": ["id"], "rows": [["value"]], "row_count": 1})
        self.assertEqual(transaction_options, [{"readonly": True}])
        connection.execute.assert_awaited_once_with("SET LOCAL statement_timeout = 10000")
        statement.fetch.assert_awaited_once_with()
        connection.close.assert_awaited_once_with()

    def test_query_keeps_the_validated_projection_without_an_internal_wildcard(self) -> None:
        sql = "SELECT id FROM public.example_safe_view LIMIT 1"
        with patch("db_query_postgresql.fetch_read_only", new_callable=AsyncMock) as fetch:
            asyncio.run(execute_query(DATABASE, sql, []))

        fetch.assert_awaited_once_with(DATABASE, sql, [])
