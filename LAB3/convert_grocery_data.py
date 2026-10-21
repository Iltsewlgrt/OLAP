"""Convert the supplied demo data to a grocery-retail subject area."""

import csv
from pathlib import Path


RAW = Path(__file__).resolve().parent / "data" / "raw"


def rewrite(name, transform):
    path = RAW / name
    with path.open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.DictReader(source))
    headers = rows[0].keys()
    for number, row in enumerate(rows, 1):
        transform(row, number)
    with path.open("w", encoding="utf-8-sig", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main():
    city = "\u0413\u0440\u043e\u0434\u043d\u043e"
    categories = [
        ("\u041c\u043e\u043b\u043e\u0447\u043d\u044b\u0435 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u044b", "\u041c\u043e\u043b\u043e\u043a\u043e"),
        ("\u0425\u043b\u0435\u0431 \u0438 \u0432\u044b\u043f\u0435\u0447\u043a\u0430", "\u0425\u043b\u0435\u0431"),
        ("\u041c\u044f\u0441\u043e \u0438 \u043f\u0442\u0438\u0446\u0430", "\u041a\u0443\u0440\u0438\u0446\u0430"),
        ("\u041e\u0432\u043e\u0449\u0438 \u0438 \u0444\u0440\u0443\u043a\u0442\u044b", "\u041e\u0432\u043e\u0449\u0438"),
        ("\u0411\u0430\u043a\u0430\u043b\u0435\u044f", "\u041a\u0440\u0443\u043f\u0430"),
        ("\u041d\u0430\u043f\u0438\u0442\u043a\u0438", "\u0421\u043e\u043a"),
        ("\u0417\u0430\u043c\u043e\u0440\u043e\u0436\u0435\u043d\u043d\u044b\u0435 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u044b", "\u041f\u043e\u043b\u0443\u0444\u0430\u0431\u0440\u0438\u043a\u0430\u0442\u044b"),
        ("\u0411\u044b\u0442\u043e\u0432\u0430\u044f \u0445\u0438\u043c\u0438\u044f", "\u0421\u0440\u0435\u0434\u0441\u0442\u0432\u043e"),
    ]
    brands = ["\u0411\u0435\u043b\u043b\u0430\u043a\u0442", "\u0421\u0430\u0432\u0443\u0448\u043a\u0438\u043d \u043f\u0440\u043e\u0434\u0443\u043a\u0442", "\u0410\u043b\u043c\u0438", "\u0411\u0430\u0431\u0443\u0448\u043a\u0438\u043d\u0430 \u043a\u0440\u044b\u043d\u043a\u0430", "\u041c\u044f\u0441\u043d\u043e\u0432\u044a"]

    rewrite("dim_store.csv", lambda row, i: row.update(
        store_name=f"\u041f\u0440\u043e\u0434\u0443\u043a\u0442\u044b \u0413\u0440\u043e\u0434\u043d\u043e \u2116{i}",
        network="\u0421\u0435\u043c\u0435\u0439\u043d\u044b\u0439 \u041c\u0430\u0440\u043a\u0435\u0442",
        city=city, region=city,
        country="\u0411\u0435\u043b\u0430\u0440\u0443\u0441\u044c", store_format="\u0421\u0443\u043f\u0435\u0440\u043c\u0430\u0440\u043a\u0435\u0442",
        logistics_center="\u0414\u0430", address=f"\u0443\u043b. \u0422\u043e\u0440\u0433\u043e\u0432\u0430\u044f, {i}, \u0413\u0440\u043e\u0434\u043d\u043e"))
    rewrite("dim_supplier.csv", lambda row, i: row.update(
        supplier_name=f"\u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u043e\u0432 {i:03d}",
        supplier_type=["\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c", "\u0414\u0438\u0441\u0442\u0440\u0438\u0431\u044c\u044e\u0442\u043e\u0440", "\u0418\u043c\u043f\u043e\u0440\u0442\u0451\u0440"][i % 3],
        country="\u0411\u0435\u043b\u0430\u0440\u0443\u0441\u044c" if i % 4 else "\u0420\u043e\u0441\u0441\u0438\u044f",
        city=city))
    rewrite("dim_warehouse.csv", lambda row, i: row.update(
        city=city, region=city, country="\u0411\u0435\u043b\u0430\u0440\u0443\u0441\u044c",
        address=f"\u0443\u043b. \u041b\u043e\u0433\u0438\u0441\u0442\u0438\u0447\u0435\u0441\u043a\u0430\u044f, {i}, \u0413\u0440\u043e\u0434\u043d\u043e"))
    rewrite("dim_employee.csv", lambda row, i: row.update(
        store_name=f"\u041f\u0440\u043e\u0434\u0443\u043a\u0442\u044b \u0413\u0440\u043e\u0434\u043d\u043e \u2116{row['store_id']}",
        region=city, country="\u0411\u0435\u043b\u0430\u0440\u0443\u0441\u044c"))
    rewrite("dim_customer.csv", lambda row, i: row.update(
        city=city, region=city, country="\u0411\u0435\u043b\u0430\u0440\u0443\u0441\u044c"))

    prices = {}
    def product(row, i):
        category, kind = categories[i % len(categories)]
        brand = brands[i % len(brands)]
        cost = round(1.2 + (i * 17 % 5000) / 100, 2)
        retail = round(cost * (1.12 + (i % 25) / 100), 2)
        row.update(article=f"GROC-{i:08d}", product_name=f"{kind} {brand} {i}",
            category=category, subcategory=kind, item_type="\u041f\u0440\u043e\u0434\u0443\u043a\u0442 \u043f\u0438\u0442\u0430\u043d\u0438\u044f",
            material=brand, metal_color="\u0423\u043f\u0430\u043a\u043e\u0432\u043a\u0430", assay="",
            weight_g=str(100 + (i % 20) * 50), size="\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442", stone="", stone_count="",
            cut="", stone_color="", clarity="", collection="\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0430\u0441\u0441\u043e\u0440\u0442\u0438\u043c\u0435\u043d\u0442",
            season="\u0412\u0441\u0435\u0441\u0435\u0437\u043e\u043d\u043d\u044b\u0439", target_gender="\u0412\u0441\u0435",
            purpose="\u041f\u0438\u0442\u0430\u043d\u0438\u0435", manufacturer_name=brand,
            cost_price=f"{cost:.2f}", retail_price=f"{retail:.2f}", currency="BYN", status="\u0412 \u043f\u0440\u043e\u0434\u0430\u0436\u0435")
        prices[int(row["product_id"])] = (cost, retail)
    rewrite("dim_product.csv", product)

    def sale(row, _):
        cost, retail = prices[int(row["product_id"])]
        number = int(row["sale_id"])
        quantity = 1 + number % 6
        discount = number % 11
        bonus = round(number % 5 * 0.25, 2)
        total = round(quantity * retail * (1 - discount / 100) - bonus, 2)
        cost_total = round(quantity * cost, 2)
        row.update(quantity=str(quantity), unit_price=f"{retail:.2f}", discount_pct=str(discount),
            bonus_used=f"{bonus:.2f}", total_amount=f"{total:.2f}", cost_amount=f"{cost_total:.2f}",
            profit_amount=f"{total - cost_total:.2f}", currency="BYN",
            payment_method="\u041d\u0430\u043b\u0438\u0447\u043d\u044b\u0435" if number % 3 == 0 else "\u0411\u0435\u0437\u043d\u0430\u043b\u0438\u0447\u043d\u044b\u0435",
            sale_type="\u041e\u0431\u044b\u0447\u043d\u0430\u044f \u043f\u0440\u043e\u0434\u0430\u0436\u0430")
    rewrite("fact_sales.csv", sale)
    rewrite("fact_visits.csv", lambda row, i: row.update(purchase_amount=f"{i % 600 / 10:.2f}"))


if __name__ == "__main__":
    main()
