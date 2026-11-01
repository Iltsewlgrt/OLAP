-- График: оборот по категориям товаров.
SELECT
    p.category,
    sum(f.total_amount) AS revenue_byn
FROM olap_product.fact_sales AS f
JOIN olap_product.dim_product AS p
    ON p.product_id = f.product_id
JOIN olap_product.dim_date AS d
    ON d.date_id = f.date_id
WHERE 1 = 1
[[ AND d.year = {{year}} ]]
GROUP BY p.category
ORDER BY revenue_byn DESC;
