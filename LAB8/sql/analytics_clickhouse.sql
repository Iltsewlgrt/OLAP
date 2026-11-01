-- З08. Аналитические запросы продуктового магазина в ClickHouse.

-- 1. Эталонная метрика: оборот.
SELECT
    sum(total_amount) AS revenue_byn
FROM olap_product.fact_sales;

-- 2. Оборот по магазинам за январь 2024 года.
SELECT
    s.region,
    s.store_name,
    round(sum(f.total_amount), 2) AS revenue_byn
FROM olap_product.fact_sales AS f
JOIN olap_product.dim_store AS s
    ON s.store_id = f.store_id
JOIN olap_product.dim_date AS d
    ON d.date_id = f.date_id
WHERE d.year = 2024
  AND d.month_num = 1
GROUP BY s.region, s.store_name
ORDER BY revenue_byn DESC, s.store_name;

-- 3. Оборот категорий и производителей за I квартал 2024 года.
WITH category_brand_revenue AS (
    SELECT
        p.category,
        p.manufacturer_name AS brand,
        sum(f.total_amount) AS revenue_byn
    FROM olap_product.fact_sales AS f
    JOIN olap_product.dim_product AS p
        ON p.product_id = f.product_id
    JOIN olap_product.dim_date AS d
        ON d.date_id = f.date_id
    WHERE d.year = 2024
      AND d.quarter = 1
    GROUP BY p.category, p.manufacturer_name
)
SELECT
    category,
    brand,
    round(revenue_byn, 2) AS revenue_byn,
    round(100.0 * revenue_byn / sum(revenue_byn) OVER (), 2) AS share_pct,
    rank() OVER (ORDER BY revenue_byn DESC) AS rank_in_quarter
FROM category_brand_revenue
ORDER BY revenue_byn DESC, category, brand;

-- 4. Средний чек по месяцам и способам оплаты.
SELECT
    d.year,
    d.month_num,
    f.payment_method,
    round(avg(f.total_amount), 2) AS avg_check_byn,
    count(*) AS sales_count
FROM olap_product.fact_sales AS f
JOIN olap_product.dim_date AS d
    ON d.date_id = f.date_id
WHERE d.year = 2024
GROUP BY d.year, d.month_num, f.payment_method
ORDER BY d.month_num, f.payment_method;
