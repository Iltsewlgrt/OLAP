"""Generate deterministic retail raw data for LAB1."""

import csv
from datetime import date, timedelta
from pathlib import Path


RAW = Path(__file__).resolve().parent / "data" / "raw"
SALES_ROWS = 30_000
STORE_COUNT = 30
PRODUCT_COUNT = 120


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)

    stores = [
        {
            "store_id": store_id,
            "store_name": f"Продукты Гродно №{store_id}",
            "city": "Гродно",
            "region": "Гродненская область",
        }
        for store_id in range(1, STORE_COUNT + 1)
    ]
    write_csv(
        RAW / "stores.csv",
        ["store_id", "store_name", "city", "region"],
        stores,
    )

    categories = [
        ("Молочные продукты", "Молоко"),
        ("Хлеб и выпечка", "Хлеб"),
        ("Мясо и птица", "Курица"),
        ("Овощи и фрукты", "Яблоки"),
        ("Бакалея", "Крупа"),
        ("Напитки", "Сок"),
        ("Замороженные продукты", "Овощная смесь"),
        ("Бытовая химия", "Средство для мытья посуды"),
    ]
    products = []
    for product_id in range(1, PRODUCT_COUNT + 1):
        category, product_type = categories[(product_id - 1) % len(categories)]
        products.append(
            {
                "product_id": product_id,
                "product_category": category,
                "product_name": f"{product_type} {product_id}",
                "unit": "шт",
                "unit_price": f"{1.50 + (product_id * 37 % 1500) / 100:.2f}",
            }
        )
    write_csv(
        RAW / "products.csv",
        ["product_id", "product_category", "product_name", "unit", "unit_price"],
        products,
    )

    payment_methods = ["card", "cash", "online"]
    start = date(2024, 1, 1)
    sales = []
    for sale_id in range(1, SALES_ROWS + 1):
        product = products[(sale_id * 17) % PRODUCT_COUNT]
        quantity = 1 + sale_id % 6
        sales.append(
            {
                "sale_id": sale_id,
                "sale_date": start + timedelta(days=(sale_id - 1) % 366),
                "store_id": 1 + (sale_id * 7) % STORE_COUNT,
                "product_category": product["product_category"],
                "product_name": product["product_name"],
                "quantity": quantity,
                "unit_price": product["unit_price"],
                "payment_method": payment_methods[sale_id % len(payment_methods)],
            }
        )
    write_csv(
        RAW / "sales.csv",
        [
            "sale_id",
            "sale_date",
            "store_id",
            "product_category",
            "product_name",
            "quantity",
            "unit_price",
            "payment_method",
        ],
        sales,
    )

    print(f"Generated {len(sales)} sales, {len(stores)} stores, {len(products)} products")


if __name__ == "__main__":
    main()
