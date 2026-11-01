# З08. Запросы и ключи ClickHouse

LAB8 проверяет, что витрина продуктового магазина из LAB7 отвечает на
аналитические вопросы, а ключ хранения и партиционирование соответствуют
рабочей нагрузке.

## Подготовка

ClickHouse из LAB1 должен быть запущен:

```powershell
cd D:\Учеба\LAB1\Стенд
docker compose up -d
```

В LAB7 перед этим должна быть выполнена загрузка:

```powershell
cd D:\Учеба\LAB7
py -3.13 etl/load_all.py
```

## Аналитические запросы

Файл [sql/analytics_clickhouse.sql](sql/analytics_clickhouse.sql) содержит:

1. эталонную метрику `SUM(total_amount)`;
2. оборот по магазинам за январь 2024 года;
3. оборот категорий с долей и рейтингом за I квартал;
4. средний чек по месяцам и способам оплаты.

Запросы можно выполнить по очереди через подготовленный Python-запускатель:

```powershell
cd D:\Учеба\LAB8
py -3.13 etl/run_sql.py sql/analytics_clickhouse.sql
```

Для быстрой проверки только эталонной метрики:

```powershell
curl.exe -u lab:lab123 --data-binary "SELECT sum(total_amount) AS revenue_byn FROM olap_product.fact_sales" http://localhost:8123/
```

Ожидаемый результат: `10750467.76`.

## Партиционирование

Файл [sql/partitioned_fact_sales.sql](sql/partitioned_fact_sales.sql):

- создаёт тестовую копию `fact_sales_partitioned`;
- делит её по месяцу через `intDiv(date_id, 100)`;
- переносит данные из `fact_sales`;
- показывает активные партиции в `system.parts`.

Запуск:

```powershell
py -3.13 etl/run_sql.py sql/partitioned_fact_sales.sql
```

Повторный запуск безопасен: скрипт сначала очищает тестовую таблицу,
затем повторно создаёт её и загружает исходные строки.

## Результаты

- [notes/queries_output.txt](notes/queries_output.txt) — результаты запросов;
- [notes/partitioned_output.txt](notes/partitioned_output.txt) — список
  месячных партиций;
- [notes/design.md](notes/design.md) — решение по `ORDER BY` и `PARTITION BY`.
