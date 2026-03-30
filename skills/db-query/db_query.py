#!/usr/bin/env python3
"""
Read-only database query executor.
Supports: PostgreSQL, MySQL, MS SQL Server.
All connections are forced read-only at the session level.
"""

import argparse
import csv
import io
import json
import sys
import yaml


def load_databases(config_path: str) -> dict:
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("databases", {})


def connect_postgresql(cfg: dict):
    import psycopg2
    conn = psycopg2.connect(
        host=cfg["host"],
        port=cfg.get("port", 5432),
        dbname=cfg["database"],
        user=cfg["username"],
        password=cfg["password"],
        options="-c default_transaction_read_only=on",
    )
    conn.set_session(readonly=True, autocommit=True)
    return conn


def connect_mysql(cfg: dict):
    import pymysql
    conn = pymysql.connect(
        host=cfg["host"],
        port=cfg.get("port", 3306),
        database=cfg["database"],
        user=cfg["username"],
        password=cfg["password"],
        cursorclass=pymysql.cursors.Cursor,
    )
    with conn.cursor() as cur:
        cur.execute("SET SESSION TRANSACTION READ ONLY")
    return conn


def connect_mssql(cfg: dict):
    import pymssql
    conn = pymssql.connect(
        server=cfg["host"],
        port=cfg.get("port", 1433),
        database=cfg["database"],
        user=cfg["username"],
        password=cfg["password"],
    )
    cursor = conn.cursor()
    cursor.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED")
    cursor.close()
    return conn


CONNECTORS = {
    "postgresql": connect_postgresql,
    "mysql": connect_mysql,
    "mssql": connect_mssql,
}


def execute_query(conn, query: str, limit: int) -> tuple[list[str], list[tuple]]:
    cursor = conn.cursor()
    cursor.execute(query)

    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    rows = cursor.fetchmany(limit) if limit > 0 else cursor.fetchall()

    cursor.close()
    return columns, rows


def format_table(columns: list[str], rows: list[tuple]) -> str:
    if not columns:
        return "(no results)"

    str_rows = [[str(v) if v is not None else "NULL" for v in row] for row in rows]
    widths = [max(len(c), *(len(r[i]) for r in str_rows) if str_rows else 0) for i, c in enumerate(columns)]

    # Recalculate widths properly
    widths = []
    for i, col in enumerate(columns):
        col_width = len(col)
        for row in str_rows:
            col_width = max(col_width, len(row[i]))
        widths.append(col_width)

    header = " | ".join(c.ljust(w) for c, w in zip(columns, widths))
    separator = "-+-".join("-" * w for w in widths)
    lines = [header, separator]
    for row in str_rows:
        lines.append(" | ".join(v.ljust(w) for v, w in zip(row, widths)))

    return "\n".join(lines)


def format_json(columns: list[str], rows: list[tuple]) -> str:
    result = [dict(zip(columns, [v for v in row])) for row in rows]
    return json.dumps(result, indent=2, default=str)


def format_csv_output(columns: list[str], rows: list[tuple]) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(columns)
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


def main():
    parser = argparse.ArgumentParser(description="Read-only database query tool")
    parser.add_argument("--config", required=True, help="Path to databases.yaml")
    parser.add_argument("--db", required=True, help="Database alias from config")
    parser.add_argument("--query", required=True, help="SQL query to execute")
    parser.add_argument("--format", choices=["table", "json", "csv"], default="table", help="Output format")
    parser.add_argument("--limit", type=int, default=100, help="Max rows to return (0 = unlimited, default 100)")
    parser.add_argument("--list-dbs", action="store_true", help="List available databases and exit")

    args = parser.parse_args()
    databases = load_databases(args.config)

    if args.list_dbs:
        if not databases:
            print("No databases configured.")
        else:
            for alias, cfg in databases.items():
                desc = cfg.get("description", "No description")
                db_type = cfg.get("type", "unknown")
                print(f"  {alias} ({db_type}): {desc}")
        return

    if args.db not in databases:
        available = ", ".join(databases.keys()) if databases else "(none)"
        print(f"Error: database '{args.db}' not found. Available: {available}", file=sys.stderr)
        sys.exit(1)

    cfg = databases[args.db]
    db_type = cfg.get("type", "postgresql")

    if db_type not in CONNECTORS:
        print(f"Error: unsupported database type '{db_type}'. Supported: {', '.join(CONNECTORS.keys())}", file=sys.stderr)
        sys.exit(1)

    # Block write operations at the application level as extra safety
    query_upper = args.query.strip().upper()
    blocked = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE", "GRANT", "REVOKE", "EXEC"]
    first_word = query_upper.split()[0] if query_upper.split() else ""
    if first_word in blocked:
        print(f"Error: write operations are not allowed. Blocked: {first_word}", file=sys.stderr)
        sys.exit(1)

    conn = None
    try:
        conn = CONNECTORS[db_type](cfg)
        columns, rows = execute_query(conn, args.query, args.limit)

        row_count = len(rows)
        if args.format == "json":
            print(format_json(columns, rows))
        elif args.format == "csv":
            print(format_csv_output(columns, rows))
        else:
            print(format_table(columns, rows))

        print(f"\n({row_count} row{'s' if row_count != 1 else ''} returned"
              + (f", limited to {args.limit}" if args.limit > 0 and row_count == args.limit else "")
              + ")")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
