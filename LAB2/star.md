# Схема «звезда»

В модели четыре таблицы фактов. Каждая имеет собственный grain:
`fact_sales` — позиция в чеке, `fact_orders` — позиция заказа,
`fact_inventory` — остаток товара на дату, `fact_logistics` — отправка по
заказу. Дата остаётся измерением `dim_date`, а не отдельным фактом.

```mermaid
erDiagram
    FACT_SALES {
        bigint sale_id PK
        bigint product_id FK
        bigint store_id FK
        bigint customer_id FK
        date sale_datetime FK
        string payment_type FK
        decimal quantity
        decimal unit_price
        decimal total_amount
    }

    FACT_ORDERS {
        bigint order_id PK
        bigint product_id FK
        bigint customer_id FK
        date order_date FK
        string payment_type FK
        decimal quantity
        decimal total_amount
    }

    FACT_INVENTORY {
        date snapshot_date FK
        bigint store_id FK
        bigint product_id FK
        decimal stock_quantity
    }

    FACT_LOGISTICS {
        bigint shipment_id PK
        bigint order_id FK
        bigint store_id FK
        date shipped_date FK
        date delivered_date FK
        decimal delivery_cost
    }

    DIM_PRODUCT {
        bigint product_id PK
        string product_name
        string category
        string brand
        string unit
        decimal price
        bigint supplier_id
    }

    DIM_STORE {
        bigint store_id PK
        string store_name
        string region
        string city
        string address
    }

    DIM_CUSTOMER {
        bigint customer_id PK
        string full_name
        string gender
        int age
        string city
        string loyalty_card
        date register_date
    }

    DIM_DATE {
        date date_key PK
        int year
        int month
        int quarter
        string weekday
    }

    DIM_PAYMENT {
        string payment_type PK
    }

    FACT_SALES }o--|| DIM_PRODUCT : "product_id"
    FACT_SALES }o--|| DIM_STORE : "store_id"
    FACT_SALES }o--|| DIM_CUSTOMER : "customer_id"
    FACT_SALES }o--|| DIM_DATE : "sale_datetime"
    FACT_SALES }o--|| DIM_PAYMENT : "payment_type"
    FACT_ORDERS }o--|| DIM_PRODUCT : "product_id"
    FACT_ORDERS }o--|| DIM_CUSTOMER : "customer_id"
    FACT_ORDERS }o--|| DIM_DATE : "order_date"
    FACT_ORDERS }o--|| DIM_PAYMENT : "payment_type"
    FACT_INVENTORY }o--|| DIM_PRODUCT : "product_id"
    FACT_INVENTORY }o--|| DIM_STORE : "store_id"
    FACT_INVENTORY }o--|| DIM_DATE : "snapshot_date"
    FACT_LOGISTICS }o--|| DIM_STORE : "store_id"
    FACT_LOGISTICS }o--|| DIM_DATE : "shipped_date"
    FACT_LOGISTICS }o--|| DIM_DATE : "delivered_date"
```

## Ключи и меры

| Таблица | Роль |
|---|---|
| `fact_sales` | продажи и меры `quantity`, `unit_price`, `total_amount` |
| `fact_orders` | заказы и заказанное количество |
| `fact_inventory` | ежедневные остатки товаров |
| `fact_logistics` | отправки, доставки и стоимость логистики |
| `dim_product` | товар, категория и бренд |
| `dim_store` | магазин, регион и город |
| `dim_customer` | клиент и программа лояльности |
| `dim_date` | календарные разрезы |
| `dim_payment` | способ оплаты |
