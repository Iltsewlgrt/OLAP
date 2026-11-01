-- З06. SCD2 для справочника продуктовых товаров.
CREATE TABLE IF NOT EXISTS dim_product_scd2 (
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
