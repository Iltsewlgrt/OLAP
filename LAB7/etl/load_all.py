"""З07. Полное обновление витрины LAB3 в ClickHouse."""

from __future__ import annotations

import re
import urllib.parse
import urllib.request
from urllib.error import HTTPError, URLError
from pathlib import Path


LAB7_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = LAB7_DIR.parent
RAW = WORKSPACE_DIR / "LAB3" / "data" / "raw"
DDL = LAB7_DIR / "sql" / "ddl_clickhouse.sql"
LOG = LAB7_DIR / "notes" / "load_log.txt"

BASE_URL = "http://localhost:8123/"
AUTH = ("lab", "lab123")
DATABASE = "olap_product"

TABLES = [
    "dim_store", "dim_warehouse", "dim_supplier", "dim_product",
    "dim_customer", "dim_employee", "dim_date",
    "fact_visits", "fact_interest", "fact_sales", "fact_loyalty",
    "fact_logistics", "fact_inventory",
]


def request(query: str, body: bytes | None = None) -> str:
    request_object = urllib.request.Request(
        BASE_URL + "?" + urllib.parse.urlencode({"query": query}),
        data=body,
        method="POST",
    )
    request_object.add_header("X-ClickHouse-User", AUTH[0])
    request_object.add_header("X-ClickHouse-Key", AUTH[1])
    try:
        with urllib.request.urlopen(request_object, timeout=60) as response:
            return response.read().decode("utf-8").strip()
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace").strip()
        raise RuntimeError(
            f"ClickHouse rejected query ({error.code}): {details or error.reason}"
        ) from error
    except URLError as error:
        raise RuntimeError(f"ClickHouse is unavailable: {error.reason}") from error


def split_sql(sql: str) -> list[str]:
    without_comments = re.sub(r"--[^\n]*", "", sql)
    return [part.strip() for part in without_comments.split(";") if part.strip()]


def create_tables() -> None:
    for statement in split_sql(DDL.read_text(encoding="utf-8")):
        request(statement)


def load_table(table: str) -> int:
    source = RAW / f"{table}.csv"
    if not source.exists():
        raise FileNotFoundError(f"CSV не найден: {source}")
    body = source.read_bytes()
    request(f"INSERT INTO {DATABASE}.{table} FORMAT CSVWithNames", body)
    return int(request(f"SELECT count() FROM {DATABASE}.{table}"))


def main() -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    create_tables()
    for table in reversed(TABLES):
        request(f"TRUNCATE TABLE {DATABASE}.{table}")

    lines = ["LOAD ORDER: " + " -> ".join(TABLES)]
    counts: dict[str, int] = {}
    for table in TABLES:
        counts[table] = load_table(table)
        lines.append(f"{table}: {counts[table]}")

    revenue = request(
        f"SELECT toString(sum(total_amount)) FROM {DATABASE}.fact_sales"
    )
    lines.append(f"CANONICAL_METRIC: SUM(total_amount) = {revenue}")
    LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
