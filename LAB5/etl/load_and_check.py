"""З05. Повторяемая загрузка витрины DuckDB с проверками качества."""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb


LAB5_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = LAB5_DIR.parent
DB = WORKSPACE_DIR / "LAB3" / "warehouse.duckdb"
RAW = WORKSPACE_DIR / "LAB3" / "data" / "raw"
DDL = WORKSPACE_DIR / "LAB3" / "sql" / "ddl_duckdb.sql"

DIMENSIONS = [
    "dim_store",
    "dim_warehouse",
    "dim_supplier",
    "dim_product",
    "dim_customer",
    "dim_employee",
    "dim_date",
]
FACTS = [
    "fact_visits",
    "fact_interest",
    "fact_sales",
    "fact_loyalty",
    "fact_logistics",
    "fact_inventory",
]
TABLES = DIMENSIONS + FACTS
DELETE_ORDER = [
    "fact_loyalty",
    "fact_interest",
    "fact_logistics",
    "fact_inventory",
    "fact_sales",
    "fact_visits",
    "dim_employee",
    "dim_product",
    "dim_customer",
    "dim_store",
    "dim_supplier",
    "dim_warehouse",
    "dim_date",
]


def fail(message: str) -> None:
    raise RuntimeError(f"FAIL: {message}")


def check_quality(con: duckdb.DuckDBPyConnection) -> None:
    nulls = con.execute(
        """
        SELECT
            COUNT(*) FILTER (WHERE sale_id IS NULL) AS null_sale_id,
            COUNT(*) FILTER (WHERE customer_id IS NULL) AS null_customer,
            COUNT(*) FILTER (WHERE product_id IS NULL) AS null_product,
            COUNT(*) FILTER (WHERE store_id IS NULL) AS null_store,
            COUNT(*) FILTER (WHERE date_id IS NULL) AS null_date,
            COUNT(*) FILTER (WHERE total_amount IS NULL) AS null_amount
        FROM fact_sales
        """
    ).fetchone()
    if any(nulls):
        fail(f"обязательные поля fact_sales содержат NULL: {nulls}")
    print("  OK nulls: fact_sales обязательные поля = 0")

    bad_ranges = con.execute(
        """
        SELECT
            COUNT(*) FILTER (WHERE quantity < 0) AS negative_quantity,
            COUNT(*) FILTER (WHERE total_amount < 0) AS negative_amount,
            COUNT(*) FILTER (WHERE date.year < 1900) AS invalid_dates
        FROM fact_sales AS f
        JOIN dim_date AS date ON date.date_id = f.date_id
        """
    ).fetchone()
    if any(bad_ranges):
        fail(f"недопустимый диапазон quantity/total_amount/date: {bad_ranges}")
    print("  OK ranges: quantity >= 0, total_amount >= 0, date >= 1900")

    duplicate_count = con.execute(
        """
        SELECT COUNT(*)
        FROM (
            SELECT sale_id
            FROM fact_sales
            GROUP BY sale_id
            HAVING COUNT(*) > 1
        )
        """
    ).fetchone()[0]
    if duplicate_count:
        fail(f"дубликаты sale_id: {duplicate_count}")
    print("  OK duplicates: sale_id unique")

    orphan_checks = {
        "store_id": """
            SELECT COUNT(*) FROM fact_sales AS f
            LEFT JOIN dim_store AS d ON d.store_id = f.store_id
            WHERE d.store_id IS NULL
        """,
        "product_id": """
            SELECT COUNT(*) FROM fact_sales AS f
            LEFT JOIN dim_product AS d ON d.product_id = f.product_id
            WHERE d.product_id IS NULL
        """,
        "date_id": """
            SELECT COUNT(*) FROM fact_sales AS f
            LEFT JOIN dim_date AS d ON d.date_id = f.date_id
            WHERE d.date_id IS NULL
        """,
    }
    for key, query in orphan_checks.items():
        count = con.execute(query).fetchone()[0]
        if count:
            fail(f"сироты по {key}: {count}")
        print(f"  OK orphans: {key} = 0")


def main() -> int:
    for path in (RAW, DDL):
        if not path.exists():
            fail(f"не найден обязательный путь: {path}")
    for table in TABLES:
        csv_path = RAW / f"{table}.csv"
        if not csv_path.exists():
            fail(f"не найден CSV: {csv_path}")

    con = duckdb.connect(str(DB))
    try:
        con.execute(DDL.read_text(encoding="utf-8"))
        con.execute("BEGIN TRANSACTION")
        try:
            for table in DELETE_ORDER:
                con.execute(f"DROP TABLE IF EXISTS {table}")
            con.execute(DDL.read_text(encoding="utf-8"))

            print("LOAD ORDER: " + " -> ".join(DIMENSIONS + FACTS))
            for table in TABLES:
                csv_path = RAW / f"{table}.csv"
                con.execute(
                    f"""
                    COPY {table} FROM '{csv_path.as_posix()}'
                    (HEADER, DELIMITER ',', QUOTE '"', ENCODING 'UTF-8')
                    """
                )

            check_quality(con)
            counts = {
                table: con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                for table in TABLES
            }
            metric, sales_rows = con.execute(
                """
                SELECT SUM(total_amount), COUNT(*)
                FROM fact_sales
                """
            ).fetchone()
            con.execute("COMMIT")
        except Exception:
            con.execute("ROLLBACK")
            raise
    finally:
        con.close()

    print("COUNTS:")
    for table, count in counts.items():
        print(f"  {table}: {count}")
    print(f"CANONICAL_METRIC: SUM(total_amount) = {metric}")
    print(f"FACT_SALES_ROWS: {sales_rows}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, duckdb.Error, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
