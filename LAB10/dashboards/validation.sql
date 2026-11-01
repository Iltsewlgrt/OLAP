-- Проверочные версии запросов для запуска вне Metabase.

SELECT sum(total_amount) AS revenue_byn
FROM olap_product.fact_sales;

SELECT
    year,
    month_num,
    sum(amount_sum) AS revenue_byn
FROM olap_product.sales_by_store_month
GROUP BY year, month_num
ORDER BY year, month_num;

SELECT
    s.store_name,
    sum(f.total_amount) AS revenue_byn
FROM olap_product.fact_sales AS f
JOIN olap_product.dim_store AS s ON s.store_id = f.store_id
GROUP BY s.store_name
ORDER BY revenue_byn DESC
LIMIT 10;

SELECT
    p.category,
    sum(f.total_amount) AS revenue_byn
FROM olap_product.fact_sales AS f
JOIN olap_product.dim_product AS p ON p.product_id = f.product_id
GROUP BY p.category
ORDER BY revenue_byn DESC;
