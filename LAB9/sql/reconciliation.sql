-- Сверка детального факта и сводной таблицы.

SELECT
    'all_data' AS check_name,
    (SELECT count() FROM olap_product.fact_sales) AS detail_rows,
    (SELECT count() FROM olap_product.sales_by_store_month) AS summary_rows,
    (SELECT sum(total_amount) FROM olap_product.fact_sales) AS detail_revenue,
    (SELECT sum(amount_sum) FROM olap_product.sales_by_store_month) AS summary_revenue;

SELECT
    'january_2024' AS check_name,
    (SELECT sum(f.total_amount)
     FROM olap_product.fact_sales AS f
     JOIN olap_product.dim_date AS d ON d.date_id = f.date_id
     WHERE d.year = 2024 AND d.month_num = 1) AS detail_revenue,
    (SELECT sum(amount_sum)
     FROM olap_product.sales_by_store_month
     WHERE year = 2024 AND month_num = 1) AS summary_revenue;
