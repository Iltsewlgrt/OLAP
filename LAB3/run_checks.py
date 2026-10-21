import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB = BASE_DIR / "warehouse.duckdb"
CHECKS = BASE_DIR / "checks.sql"
OUTPUT = BASE_DIR / "checks.txt"

if not DB.exists():
    raise SystemExit("warehouse.duckdb not found. Run load_data.py first.")

con = duckdb.connect(str(DB), read_only=True)
try:
    statements = [
        statement.strip()
        for statement in CHECKS.read_text(encoding="utf-8-sig").split(";")
        if statement.strip()
    ]
    outputs = []
    for number, statement in enumerate(statements, start=1):
        result = con.execute(statement).fetchall()
        columns = [column[0] for column in con.description]
        outputs.append((number, columns, result))
finally:
    con.close()

with OUTPUT.open("w", encoding="utf-8-sig", newline="") as output:
    for number, columns, rows in outputs:
        output.write(f"-- query {number}\n")
        output.write("\t".join(columns) + "\n")
        for row in rows:
            output.write(
                "\t".join("" if value is None else str(value) for value in row) + "\n"
            )
        output.write("\n")

print(f"{OUTPUT.name} written (UTF-8, replaced)")
