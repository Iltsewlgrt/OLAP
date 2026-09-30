# Учебный стенд

Стенд поднимает ClickHouse и Metabase через Docker Compose.

## Требования

- Docker Desktop;
- Git Bash или WSL для запуска `init_ch.sh`;
- Python 3.10+ для DuckDB smoke-проверки.

## Запуск

Из этой папки:

```bash
docker compose up -d
./scripts/init_ch.sh
curl http://localhost:8123/ping
```

Скрипт ожидает готовности ClickHouse, подключается пользователем `lab` с паролем `lab123`, создаёт базу `lab`, таблицу `lab.raw_sales` и загружает файл `../data/raw/sales.csv`.

Проверка данных:

```bash
curl -u lab:lab123 'http://localhost:8123/?query=SELECT%20count()%20FROM%20lab.raw_sales'
```

Ожидаемый результат: `10`.

## DuckDB smoke

Из корня проекта установите зависимость:

```bash
python -m pip install -r Стенд/requirements.txt
duckdb -c "SELECT COUNT(*) AS rows, ROUND(SUM(quantity * unit_price), 2) AS revenue FROM read_csv_auto('data/raw/sales.csv');"
```

Ожидаемый результат: `10` строк и `3246.30` выручки.
