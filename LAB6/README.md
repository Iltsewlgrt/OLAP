# З06. SCD2 для товаров

В лабораторной реализовано хранение истории справочника `dim_product` для
продуктового магазина. SCD2 нужен, чтобы изменение категории или цены товара
не переписывалось задним числом в старых продажах.

## Что сделано

Добавлены поля:

- `valid_from` — дата начала действия версии;
- `valid_to` — дата окончания версии, не включая эту дату;
- `is_current` — признак актуальной версии.

Для демонстрации товар `product_id = 1` меняет категорию:

```text
2020-01-01 — 2024-02-01: Хлеб и выпечка
2024-02-01 — 9999-12-31: Готовая выпечка
```

Это изменение подходит для продуктового магазина: товар остаётся тем же,
но его ассортиментная категория уточняется.

## Запуск

Команды выполняются из папки `D:\Учеба\OLAP\LAB6`:

```powershell
py -3.13 -m pip install duckdb
py -3.13 -c "import duckdb; c=duckdb.connect('scd2_demo.duckdb'); sql=open('sql/demo_scd2.sql', encoding='utf-8').read(); print(c.execute(sql).fetchall()); c.close()"
```

Для удобного чтения всех результатов:

```powershell
@'
import duckdb
from pathlib import Path

connection = duckdb.connect("scd2_demo.duckdb")
sql = Path("sql/demo_scd2.sql").read_text(encoding="utf-8")

for number, query in enumerate(
    part.strip() for part in sql.split(";") if part.strip(), start=1
):
    result = connection.execute(query)
    if result.description:
        print(f"\nЗапрос {number}:")
        print([column[0] for column in result.description])
        for row in result.fetchall():
            print(row)

connection.close()
'@ | py -3.13 -
```

## Как подключаются продажи

Для продажи выбирается версия товара по условию:

```sql
valid_from <= sale_date
AND sale_date < valid_to
```

Поэтому продажа от `2024-01-15` относится к категории «Хлеб и выпечка», а
продажа от `2024-02-15` — к категории «Готовая выпечка».

DDL находится в [sql/ddl_scd2.sql](sql/ddl_scd2.sql), демонстрация — в
[sql/demo_scd2.sql](sql/demo_scd2.sql), результаты — в
[scd2_output.txt](scd2_output.txt).
