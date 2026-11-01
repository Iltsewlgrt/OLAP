# З07. Данные в ClickHouse

LAB7 переносит витрину продуктового магазина из LAB3 в ClickHouse. В ClickHouse
загружаются 13 таблиц: 7 измерений и 6 фактов. Деньги хранятся в
`Decimal(14, 2)`, а не в `Float`.

## Подготовка стенда

Из папки `D:\Учеба\LAB1\Стенд` запустите ClickHouse:

```powershell
docker compose up -d
```

Проверка доступности:

```powershell
curl.exe http://localhost:8123/ping
```

Ожидаемый ответ:

```text
Ok.
```

## Загрузка

Из папки `D:\Учеба\LAB7` выполните:

```powershell
py -3.13 etl/load_all.py
```

Скрипт создаёт базу `olap_product`, создаёт таблицы по
[sql/ddl_clickhouse.sql](sql/ddl_clickhouse.sql), очищает старые строки и
загружает CSV из `LAB3/data/raw/`.

Повторный запуск безопасен: используется полный refresh — перед загрузкой
таблицы очищаются. Поэтому `fact_sales` не превращается в 200 000 строк.

## Сверка

Проверка в ClickHouse:

```powershell
curl.exe -u lab:lab123 "http://localhost:8123/?query=SELECT%20count()%20FROM%20olap_product.fact_sales"
curl.exe -u lab:lab123 "http://localhost:8123/?query=SELECT%20sum(total_amount)%20FROM%20olap_product.fact_sales"
```

Ожидаемый результат:

```text
100000
10750467.76
```

Лог загрузки сохраняется в [notes/load_log.txt](notes/load_log.txt), описание
порядка хранения — в [notes/design.md](notes/design.md), сверка — в
[notes/reconciliation.md](notes/reconciliation.md).
