-- Полный пересчёт сводки после загрузки детального факта.

TRUNCATE TABLE olap_product.sales_by_store_month;

INSERT INTO olap_product.sales_by_store_month
SELECT
    d.year,
    d.month_num,
    f.store_id,
    s.store_name,
    sum(f.total_amount) AS amount_sum
FROM olap_product.fact_sales AS f
JOIN olap_product.dim_store AS s
    ON s.store_id = f.store_id
JOIN olap_product.dim_date AS d
    ON d.date_id = f.date_id
GROUP BY d.year, d.month_num, f.store_id, s.store_name;
