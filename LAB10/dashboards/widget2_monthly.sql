-- График: оборот по месяцам.
SELECT
    year,
    month_num,
    concat(toString(year), '-', leftPad(toString(month_num), 2, '0')) AS month,
    sum(amount_sum) AS revenue_byn
FROM olap_product.sales_by_store_month
WHERE 1 = 1
[[ AND year = {{year}} ]]
GROUP BY year, month_num
ORDER BY year, month_num;
