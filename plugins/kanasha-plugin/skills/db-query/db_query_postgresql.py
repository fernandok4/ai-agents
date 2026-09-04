"""Adaptador PostgreSQL do broker; este módulo é o único que abre conexões."""

from datetime import date, datetime, time
from decimal import Decimal
from uuid import UUID


async def execute_query(database: dict[str, object], sql: str, params: list[object]) -> dict[str, object]:
    return await fetch_read_only(database, sql, params)


async def describe_relation(database: dict[str, object], schema: str, relation: str) -> dict[str, object]:
    metadata_sql = (
        "SELECT column_name, data_type, is_nullable, ordinal_position "
        "FROM information_schema.columns "
        "WHERE table_schema = $1 AND table_name = $2 "
        "ORDER BY ordinal_position"
    )
    return await fetch_read_only(database, metadata_sql, [schema, relation])


async def fetch_read_only(database: dict[str, object], sql: str, params: list[object]) -> dict[str, object]:
    import asyncpg

    connection = await asyncpg.connect(
        host=str(database["host"]),
        port=int(database["port"]),
        database=str(database["database"]),
        user=str(database["username"]),
        password=str(database["password"]),
        timeout=int(database["connect_timeout_seconds"]),
        command_timeout=int(database["statement_timeout_ms"]) / 1_000,
    )
    try:
        async with connection.transaction(readonly=True):
            await connection.execute(f"SET LOCAL statement_timeout = {int(database['statement_timeout_ms'])}")
            statement = await connection.prepare(sql)
            records = await statement.fetch(*params)
            columns = [attribute.name for attribute in statement.get_attributes()]
    finally:
        await connection.close()

    rows = [[json_value(value) for value in record.values()] for record in records]
    return {"columns": columns, "rows": rows, "row_count": len(rows)}


def json_value(value: object) -> object:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (date, datetime, time, Decimal, UUID)):
        return str(value)
    return str(value)
