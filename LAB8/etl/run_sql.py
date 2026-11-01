from __future__ import annotations

import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


BASE_URL = "http://localhost:8123/"
AUTH = ("lab", "lab123")


def split_sql(text: str) -> list[str]:
    text_without_comments = re.sub(r"--[^\n]*", "", text)
    return [statement.strip() for statement in text_without_comments.split(";") if statement.strip()]


def execute(statement: str) -> str:
    request = urllib.request.Request(
        BASE_URL + "?" + urllib.parse.urlencode({"query": statement}),
        method="POST",
    )
    request.add_header("X-ClickHouse-User", AUTH[0])
    request.add_header("X-ClickHouse-Key", AUTH[1])
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8").strip()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: py -3.13 etl/run_sql.py <sql-file>")

    sql_file = Path(sys.argv[1])
    output_lines: list[str] = []
    for number, statement in enumerate(split_sql(sql_file.read_text(encoding="utf-8")), 1):
        output_lines.append(f"--- statement {number} ---")
        result = execute(statement)
        if result:
            output_lines.append(result)

    output = "\n".join(output_lines) + "\n"
    print(output, end="")
    if sql_file.name == "analytics_clickhouse.sql":
        (sql_file.parents[1] / "notes" / "queries_output.txt").write_text(
            output, encoding="utf-8"
        )
    elif sql_file.name == "partitioned_fact_sales.sql":
        (sql_file.parents[1] / "notes" / "partitioned_output.txt").write_text(
            output, encoding="utf-8"
        )


if __name__ == "__main__":
    main()
