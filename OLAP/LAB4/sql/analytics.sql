-- З04. Аналитический SQL для витрины LAB3.
-- Скрипт рассчитан на LAB3/warehouse.duckdb.

-- Вопрос 1: какой оборот по регионам и магазинам за январь 2024 года?
SELECT
    s.region,
    s.store_name,
    ROUND(SUM(f.total_amount), 2) AS revenue_byn
FROM fact_sales AS f
JOIN dim_store AS s
    ON s.store_id = f.store_id
JOIN dim_date AS d
    ON d.date_id = f.date_id
WHERE d.year = 2024
  AND d.month_num = 1
GROUP BY s.region, s.store_name
ORDER BY revenue_byn DESC, s.store_name;

-- Вопрос 2: какие категории и бренды дают наибольший оборот за первый квартал?
-- Оконные функции показывают долю строки в обороте квартала и её место.
WITH category_brand_revenue AS (
    SELECT
        p.category,
        p.manufacturer_name AS brand,
        SUM(f.total_amount) AS revenue_byn
    FROM fact_sales AS f
    JOIN dim_product AS p
        ON p.product_id = f.product_id
    JOIN dim_date AS d
        ON d.date_id = f.date_id
    WHERE d.year = 2024
      AND d.quarter = 1
    GROUP BY p.category, p.manufacturer_name
)
SELECT
    category,
    brand,
    ROUND(revenue_byn, 2) AS revenue_byn,
    ROUND(100.0 * revenue_byn / SUM(revenue_byn) OVER (), 2) AS share_pct,
    RANK() OVER (ORDER BY revenue_byn DESC) AS rank_in_quarter
FROM category_brand_revenue
ORDER BY revenue_byn DESC, category, brand;

-- Вопрос 3: как меняются количество единиц и средний чек по месяцам
-- и способам оплаты?
WITH receipts AS (
    SELECT
        d.year,
        d.month_num,
        f.payment_method,
        f.receipt_number,
        SUM(f.quantity) AS receipt_quantity,
        SUM(f.total_amount) AS receipt_amount
    FROM fact_sales AS f
    JOIN dim_date AS d
        ON d.date_id = f.date_id
    WHERE d.year = 2024
    GROUP BY
        d.year,
        d.month_num,
        f.payment_method,
        f.receipt_number
)
SELECT
    year,
    month_num,
    payment_method,
    SUM(receipt_quantity) AS units_sold,
    COUNT(*) AS receipt_count,
    ROUND(AVG(receipt_amount), 2) AS avg_check_byn
FROM receipts
GROUP BY year, month_num, payment_method
ORDER BY month_num, payment_method;
