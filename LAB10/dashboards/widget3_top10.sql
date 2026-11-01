-- График: топ-10 магазинов по обороту.
SELECT
    s.store_name,
    sum(f.total_amount) AS revenue_byn
FROM olap_product.fact_sales AS f
JOIN olap_product.dim_store AS s
    ON s.store_id = f.store_id
JOIN olap_product.dim_date AS d
    ON d.date_id = f.date_id
WHERE 1 = 1
[[ AND d.year = {{year}} ]]
GROUP BY s.store_name
ORDER BY revenue_byn DESC
LIMIT 10;
