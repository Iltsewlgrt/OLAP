-- Главная метрика: оборот без возвратов.
-- В текущем сырье возвраты не выделены, поэтому используется весь fact_sales.
SELECT SUM(total_amount) AS revenue_byn
FROM fact_sales;
