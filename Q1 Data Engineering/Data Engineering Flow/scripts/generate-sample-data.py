"""Generate sample retail CSV datasets for local notebook testing."""
from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "sample"
OUT.mkdir(parents=True, exist_ok=True)

random.seed(42)

STORES = [
    ("S001", "Downtown Flagship", "Seattle", "WA", "98101", "West", 4200000),
    ("S002", "Mall of Bellevue", "Bellevue", "WA", "98004", "West", 3800000),
    ("S003", "Portland Pioneer", "Portland", "OR", "97201", "West", 5100000),
    ("S004", "Denver Union", "Denver", "CO", "80202", "Mountain", 2900000),
    ("S005", "Chicago Loop", "Chicago", "IL", "60601", "Midwest", 6100000),
]

PRODUCTS = [
    ("P1001", "Organic Cotton T-Shirt", "Apparel", "Basics", 24.99),
    ("P1002", "Denim Jeans Slim Fit", "Apparel", "Denim", 59.99),
    ("P1003", "Running Sneakers Pro", "Footwear", "Athletic", 89.99),
    ("P1004", "Leather Crossbody Bag", "Accessories", "Bags", 79.99),
    ("P1005", "Wireless Earbuds", "Electronics", "Audio", 129.99),
    ("P1006", "Stainless Water Bottle", "Home", "Kitchen", 19.99),
    ("P1007", "Yoga Mat Premium", "Sports", "Fitness", 34.99),
    ("P1008", "Winter Puffer Jacket", "Apparel", "Outerwear", 149.99),
]

CUSTOMERS = [
    ("C0001", "Alice", "Johnson", "alice.j@email.com", "Gold", "2022-03-15"),
    ("C0002", "Bob", "Smith", "bob.s@email.com", "Silver", "2023-01-20"),
    ("C0003", "Carol", "Williams", "carol.w@email.com", "Bronze", "2024-06-01"),
    ("C0004", "David", "Brown", "david.b@email.com", "Gold", "2021-11-08"),
    ("C0005", "Eva", "Martinez", "eva.m@email.com", "Silver", "2023-09-12"),
    ("C0006", "Frank", "Lee", "frank.l@email.com", "Bronze", "2024-02-28"),
    ("C0007", "Grace", "Taylor", "grace.t@email.com", "Platinum", "2020-05-30"),
    ("C0008", "Henry", "Anderson", "henry.a@email.com", "Silver", "2023-04-17"),
]


def write_csv(name: str, headers: list[str], rows: list[list]) -> None:
    path = OUT / name
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Wrote {path} ({len(rows)} rows)")


def gen_stores() -> None:
    write_csv(
        "stores.csv",
        ["store_id", "store_name", "city", "state", "postal_code", "region", "opened_date", "annual_sales_usd"],
        [[s[0], s[1], s[2], s[3], s[4], s[5], "2018-01-01", s[6]] for s in STORES],
    )


def gen_products() -> None:
    write_csv(
        "products.csv",
        ["product_id", "product_name", "category", "subcategory", "unit_price", "is_active"],
        [[p[0], p[1], p[2], p[3], p[4], "Y"] for p in PRODUCTS],
    )


def gen_customers() -> None:
    write_csv(
        "customers.csv",
        ["customer_id", "first_name", "last_name", "email", "loyalty_tier", "signup_date"],
        [list(c) for c in CUSTOMERS],
    )
    import json
    payload = [
        {
            "customer_id": c[0],
            "first_name": c[1],
            "last_name": c[2],
            "email": c[3],
            "loyalty_tier": c[4],
            "signup_date": c[5],
        }
        for c in CUSTOMERS
    ]
    json_path = OUT / "customers.json"
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {json_path} ({len(payload)} rows)")


def gen_inventory() -> None:
    rows = []
    as_of = datetime(2025, 5, 31).date().isoformat()
    for store_id, *_ in STORES:
        for product_id, *_ in PRODUCTS:
            qty = random.randint(0, 200)
            reorder = random.randint(10, 30)
            rows.append([store_id, product_id, qty, reorder, as_of])
    write_csv(
        "inventory.csv",
        ["store_id", "product_id", "quantity_on_hand", "reorder_point", "snapshot_date"],
        rows,
    )


def gen_pos_transactions() -> None:
    rows = []
    base = datetime(2025, 5, 1)
    txn_id = 10000
    for day in range(30):
        dt = base + timedelta(days=day)
        for _ in range(random.randint(8, 15)):
            txn_id += 1
            store = random.choice(STORES)
            customer = random.choice(CUSTOMERS)
            product = random.choice(PRODUCTS)
            qty = random.randint(1, 3)
            unit_price = product[4]
            discount = round(random.choice([0, 0, 0, 5, 10, 15]), 2)
            line_total = round(qty * unit_price * (1 - discount / 100), 2)
            rows.append([
                f"T{txn_id}",
                dt.strftime("%Y-%m-%d"),
                dt.strftime("%H:%M:%S"),
                store[0],
                customer[0],
                product[0],
                qty,
                unit_price,
                discount,
                line_total,
                random.choice(["CREDIT", "DEBIT", "CASH", "MOBILE"]),
            ])
    write_csv(
        "pos_transactions.csv",
        [
            "transaction_id", "transaction_date", "transaction_time",
            "store_id", "customer_id", "product_id", "quantity",
            "unit_price", "discount_pct", "line_total", "payment_method",
        ],
        rows,
    )


if __name__ == "__main__":
    gen_stores()
    gen_products()
    gen_customers()
    gen_inventory()
    gen_pos_transactions()
    print("Sample retail datasets generated.")
