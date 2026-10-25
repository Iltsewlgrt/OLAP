# З04. Аналитический SQL

Запросы используют витрину из `LAB3/warehouse.duckdb`:

- `sql/analytics.sql` содержит ответы на три бизнес-вопроса из паспорта;
- `sql/canonical_metric.sql` содержит эталон расчёта главной метрики;
- паспорт с тем же текстом эталонного SQL обновлён в `LAB2/passport.md`.

Запуск из корня репозитория:

```powershell
py -3.13 -c "import duckdb; c=duckdb.connect('LAB3/warehouse.duckdb'); print(c.execute(open('LAB4/sql/canonical_metric.sql', encoding='utf-8').read()).fetchall()); c.close()"
```

`analytics.sql` содержит несколько `SELECT`, поэтому его удобно выполнять
в DuckDB CLI или в клиенте DuckDB по отдельным блокам.
