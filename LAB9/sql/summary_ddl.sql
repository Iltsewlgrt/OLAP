-- Сводка для графика «Оборот по месяцам и магазинам».
-- Одна строка = один месяц + один магазин.

CREATE DATABASE IF NOT EXISTS olap_product;

CREATE TABLE IF NOT EXISTS olap_product.sales_by_store_month
(
    year Int32,
    month_num Int32,
    store_id Int32,
    store_name String,
    amount_sum Decimal(18, 2)
)
ENGINE = MergeTree
ORDER BY (year, month_num, store_id);
