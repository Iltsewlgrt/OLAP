#!/usr/bin/env bash
set -euo pipefail

CLICKHOUSE_URL="http://localhost:8123/"
CLICKHOUSE_USER="lab"
CLICKHOUSE_PASSWORD="lab123"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RAW_FILE="${PROJECT_ROOT}/data/raw/sales.csv"

until curl --fail --silent "${CLICKHOUSE_URL}ping" >/dev/null; do
  sleep 2
done

run_query() {
  curl --fail --silent --show-error --user "${CLICKHOUSE_USER}:${CLICKHOUSE_PASSWORD}" --data-binary "$1" "${CLICKHOUSE_URL}"
}

run_query "CREATE DATABASE IF NOT EXISTS lab"
run_query "CREATE TABLE IF NOT EXISTS lab.raw_sales (sale_id UInt32, sale_date Date, store_id UInt32, product_category String, product_name String, quantity UInt32, unit_price Decimal(12, 2), payment_method String) ENGINE = MergeTree ORDER BY (sale_date, sale_id)"
run_query "TRUNCATE TABLE lab.raw_sales"
curl --fail --silent --show-error --user "${CLICKHOUSE_USER}:${CLICKHOUSE_PASSWORD}" --data-binary "@${RAW_FILE}" "${CLICKHOUSE_URL}?query=INSERT%20INTO%20lab.raw_sales%20FORMAT%20CSVWithNames"

printf 'ClickHouse is initialized. Rows: '
run_query "SELECT count() FROM lab.raw_sales"
