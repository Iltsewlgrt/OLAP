# З09. Сводная витрина ClickHouse

LAB9 создаёт сводную таблицу для будущего графика «Оборот по месяцам и
магазинам» в продуктовой сети.

## Смысл строки

Одна строка `sales_by_store_month` = один месяц + один магазин. В строке
хранятся год, месяц, идентификатор магазина, название магазина и готовая сумма
оборота `amount_sum`.

## Запуск

ClickHouse и данные LAB7 должны быть загружены заранее:

```powershell
cd D:\Учеба\LAB1\Стенд
docker compose up -d

cd D:\Учеба\LAB7
py -3.13 etl\load_all.py
```

Создание и полное заполнение сводки:

```powershell
cd D:\Учеба\LAB9
py -3.13 etl\run_sql.py sql\summary_ddl.sql
py -3.13 etl\run_sql.py sql\summary_fill.sql
py -3.13 etl\run_sql.py sql\reconciliation.sql
```

`summary_fill.sql` использует `TRUNCATE + INSERT SELECT`, поэтому после
повторной загрузки детального факта сводка пересобирается без накопления
дубликатов.

## Результаты

- [notes/z09.md](notes/z09.md) — описание графика и правила пересчёта;
- [notes/console_proof.txt](notes/console_proof.txt) — фактическая сверка;
- [sql/summary_ddl.sql](sql/summary_ddl.sql) — DDL сводной таблицы;
- [sql/summary_fill.sql](sql/summary_fill.sql) — заполнение сводки;
- [sql/reconciliation.sql](sql/reconciliation.sql) — запросы сверки.
