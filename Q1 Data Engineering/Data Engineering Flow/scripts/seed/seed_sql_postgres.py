"""Seed Azure SQL or PostgreSQL from generated .sql files (fallback when sqlcmd/psql missing)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def split_batches(sql: str) -> list[str]:
    parts = re.split(r";\s*\n", sql.strip())
    return [p.strip() + ";" for p in parts if p.strip()]


def run_sqlserver(server: str, database: str, user: str, password: str, sql_file: Path) -> None:
    sql = sql_file.read_text(encoding="utf-8")
    try:
        import pyodbc
        for driver in ("ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server", "SQL Server"):
            try:
                conn_str = (
                    f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};"
                    f"UID={user};PWD={password};Encrypt=yes;TrustServerCertificate=no;"
                )
                with pyodbc.connect(conn_str) as conn:
                    cur = conn.cursor()
                    for batch in split_batches(sql):
                        cur.execute(batch)
                    conn.commit()
                print(f"SQL Server seed complete from {sql_file.name} (driver: {driver})")
                return
            except pyodbc.Error:
                continue
    except ImportError:
        pass
    try:
        import pymssql
        conn = pymssql.connect(server=server, user=user, password=password, database=database)
        try:
            with conn.cursor() as cur:
                for batch in split_batches(sql):
                    cur.execute(batch)
            conn.commit()
        finally:
            conn.close()
        print(f"SQL Server seed complete from {sql_file.name} (pymssql)")
        return
    except ImportError:
        print("Install pyodbc or pymssql for SQL seed fallback", file=sys.stderr)
        sys.exit(1)


def run_postgres(host: str, database: str, user: str, password: str, sql_file: Path) -> None:
    try:
        import psycopg2
    except ImportError:
        print("Install psycopg2-binary: pip install psycopg2-binary", file=sys.stderr)
        sys.exit(1)
    sql = sql_file.read_text(encoding="utf-8")
    conn = psycopg2.connect(host=host, dbname=database, user=user, password=password, sslmode="require")
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    finally:
        conn.close()
    print(f"PostgreSQL seed complete from {sql_file.name}")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--target", choices=["sql", "postgres"], required=True)
    p.add_argument("--server", required=True)
    p.add_argument("--database", required=True)
    p.add_argument("--user", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--file", required=True)
    args = p.parse_args()
    if not args.password:
        print("Password required", file=sys.stderr)
        sys.exit(1)
    path = Path(args.file)
    if args.target == "sql":
        run_sqlserver(args.server, args.database, args.user, args.password, path)
    else:
        run_postgres(args.server, args.database, args.user, args.password, path)


if __name__ == "__main__":
    main()
