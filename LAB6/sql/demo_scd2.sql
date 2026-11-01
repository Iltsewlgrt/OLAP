-- З06. Демонстрация SCD2 для продуктового магазина.
-- Товар product_id = 1 меняет категорию 2024-02-01.

DROP TABLE IF EXISTS dim_product_scd2;
CREATE TABLE dim_product_scd2 (
    product_version_id INTEGER PRIMARY KEY,
    product_id         INTEGER NOT NULL,
    product_name       VARCHAR NOT NULL,
    category           VARCHAR NOT NULL,
    manufacturer_name  VARCHAR,
    retail_price       DECIMAL(14, 2),
    valid_from         DATE NOT NULL,
    valid_to           DATE NOT NULL,
    is_current         BOOLEAN NOT NULL,
    CHECK (valid_from < valid_to)
);

INSERT INTO dim_product_scd2 VALUES
    (1, 1, 'Хлеб Савушкин продукт 1', 'Хлеб и выпечка',
     'Савушкин продукт', 1.55, DATE '2020-01-01', DATE '2024-02-01', false),
    (2, 2, 'Курица Алми 2', 'Мясо и птица',
     'Алми', 1.76, DATE '2020-01-01', DATE '9999-12-31', true),
    (3, 3, 'Овощи Бабушкина крынка 3', 'Овощи и фрукты',
     'Бабушкина крынка', 1.97, DATE '2020-01-01', DATE '9999-12-31', true),
    (4, 4, 'Крупа Мясновъ 4', 'Бакалея',
     'Мясновъ', 2.18, DATE '2020-01-01', DATE '9999-12-31', true),
    (5, 5, 'Сок Добрый 5', 'Напитки',
     'Добрый', 2.40, DATE '2020-01-01', DATE '9999-12-31', true),
    (6, 1, 'Хлеб Савушкин продукт 1', 'Готовая выпечка',
     'Савушкин продукт', 1.70, DATE '2024-02-01', DATE '9999-12-31', true);

-- Показать две версии одного товара.
SELECT
    product_id,
    product_name,
    category,
    manufacturer_name,
    retail_price,
    valid_from,
    valid_to,
    is_current
FROM dim_product_scd2
WHERE product_id = 1
ORDER BY valid_from;

-- Факт соединяется с версией по дате события:
-- valid_from <= sale_date AND sale_date < valid_to.
SELECT
    DATE '2024-01-15' AS sale_date,
    p.product_id,
    p.category
FROM dim_product_scd2 AS p
WHERE p.product_id = 1
  AND DATE '2024-01-15' >= p.valid_from
  AND DATE '2024-01-15' < p.valid_to
UNION ALL
SELECT
    DATE '2024-02-15' AS sale_date,
    p.product_id,
    p.category
FROM dim_product_scd2 AS p
WHERE p.product_id = 1
  AND DATE '2024-02-15' >= p.valid_from
  AND DATE '2024-02-15' < p.valid_to
ORDER BY sale_date;

SELECT
    COUNT(*) AS total_versions,
    COUNT(DISTINCT product_id) AS unique_products,
    COUNT(*) FILTER (WHERE is_current) AS current_versions
FROM dim_product_scd2;
