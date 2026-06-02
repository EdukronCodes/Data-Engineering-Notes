"""Generate SQL seed scripts and REST JSON from data/sample CSVs."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "data" / "sample"
SEED = Path(__file__).resolve().parent


def read_csv(name: str) -> list[dict]:
    with (SAMPLE / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sql_str(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


def build_pos_sql() -> None:
    rows = read_csv("pos_transactions.csv")
    lines = [
        "IF OBJECT_ID('dbo.pos_transactions', 'U') IS NOT NULL DROP TABLE dbo.pos_transactions;",
        "CREATE TABLE dbo.pos_transactions (",
        "  transaction_id NVARCHAR(32) NOT NULL,",
        "  transaction_date DATE NOT NULL,",
        "  transaction_time NVARCHAR(16),",
        "  store_id NVARCHAR(16),",
        "  customer_id NVARCHAR(16),",
        "  product_id NVARCHAR(16),",
        "  quantity INT,",
        "  unit_price DECIMAL(10,2),",
        "  discount_pct DECIMAL(5,2),",
        "  line_total DECIMAL(12,2),",
        "  payment_method NVARCHAR(16)",
        ");",
        "INSERT INTO dbo.pos_transactions VALUES",
    ]
    values = []
    for r in rows:
        values.append(
            f"({sql_str(r['transaction_id'])},{sql_str(r['transaction_date'])},"
            f"{sql_str(r['transaction_time'])},{sql_str(r['store_id'])},"
            f"{sql_str(r['customer_id'])},{sql_str(r['product_id'])},"
            f"{r['quantity']},{r['unit_price']},{r['discount_pct']},"
            f"{r['line_total']},{sql_str(r['payment_method'])})"
        )
    lines.append(",\n".join(values) + ";")
    out = SEED / "pos_transactions.sql"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out} ({len(rows)} POS rows)")


def build_inventory_sql() -> None:
    rows = read_csv("inventory.csv")
    lines = [
        "DROP TABLE IF EXISTS inventory_snapshot;",
        "CREATE TABLE inventory_snapshot (",
        "  store_id VARCHAR(16),",
        "  product_id VARCHAR(16),",
        "  quantity_on_hand INT,",
        "  reorder_point INT,",
        "  snapshot_date DATE",
        ");",
        "INSERT INTO inventory_snapshot VALUES",
    ]
    values = []
    for r in rows:
        values.append(
            f"({sql_str(r['store_id'])},{sql_str(r['product_id'])},"
            f"{r['quantity_on_hand']},{r['reorder_point']},{sql_str(r['snapshot_date'])})"
        )
    lines.append(",\n".join(values) + ";")
    out = SEED / "inventory.sql"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out} ({len(rows)} inventory rows)")


def build_customers_json() -> None:
    rows = read_csv("customers.csv")
    payload = [
        {
            "customer_id": r["customer_id"],
            "first_name": r["first_name"],
            "last_name": r["last_name"],
            "email": r["email"],
            "loyalty_tier": r["loyalty_tier"],
            "signup_date": r["signup_date"],
        }
        for r in rows
    ]
    out = SAMPLE / "customers.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {out} ({len(payload)} customers)")


if __name__ == "__main__":
    build_pos_sql()
    build_inventory_sql()
    build_customers_json()
