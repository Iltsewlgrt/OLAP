# З01. Стенд и сырьё

## Команда

| Участник | Зона ответственности | Что запушить в GitHub |
|---|---|---|
| Участник 1: `Бальцевич Анна Ивановна` | Docker Compose, ClickHouse, инициализация и проверка `ping` | `Стенд/docker-compose.yml`, `Стенд/scripts/init_ch.sh`, `Стенд/README.md`; коммит `feat: add docker analytics stand` |
| Участник 2: `Лобзик Виктория Александровна` | Тема проекта и подготовка исходного CSV | `data/raw/sales.csv`; раздел «Сырьё»; коммит `feat: add raw retail sales data` |
| Участник 3: `Ерофеева Валерия Евгеньевна` | DuckDB smoke-проверка и общая документация | `README.md`; коммит `docs: document lab 01 and team workflow` |

## Тема проекта

**Розничные продажи в магазине.** В следующих лабораторных работах будем считать выручку, средний чек, продажи по категориям и показатели магазинов.

Файл сырья синтетический, создан для учебной работы и не содержит персональных данных.

## Состав проекта

```text
.
├── 01_З01_стенд_и_сырьё.md
├── README.md
├── data/
│   └── raw/
│       └── sales.csv
└── Стенд/
    ├── README.md
    ├── docker-compose.yml
    └── scripts/
        └── init_ch.sh
```

## Запуск ClickHouse и Metabase

Требования: Docker Desktop и Git Bash или WSL.

```bash
cd Стенд
docker compose up -d
./scripts/init_ch.sh
curl http://localhost:8123/ping
```

Ожидаемый ответ:

```text
Ok.
```

Порты:

- ClickHouse HTTP: `8123`;
- ClickHouse native: `9000`;
- Metabase web-интерфейс: `3000`.

После инициализации можно проверить количество строк. Для SQL-запросов используется учебная пара `lab` / `lab123`:

```bash
curl -u lab:lab123 'http://localhost:8123/?query=SELECT%20count()%20FROM%20lab.raw_sales'
```

Ожидаемый результат: `10`.

Остановка стенда:

```bash
docker compose down
```

## Проверка DuckDB

Инструкция находится в [Стенд/README.md](Стенд/README.md). Минимальная проверка читает тот же локальный CSV и не требует ClickHouse:

```bash
python -m pip install -r Стенд/requirements.txt
duckdb -c "SELECT COUNT(*) AS rows, ROUND(SUM(quantity * unit_price), 2) AS revenue FROM read_csv_auto('data/raw/sales.csv');"
```

Ожидаемый результат: `10` строк и выручка `3246.30`.

## Сырьё

Исходный файл: [data/raw/sales.csv](data/raw/sales.csv). В нём 10 строк и 8 колонок:

| Колонка | Описание |
|---|---|
| `sale_id` | Уникальный идентификатор продажи |
| `sale_date` | Дата продажи в формате `YYYY-MM-DD` |
| `store_id` | Идентификатор магазина |
| `product_category` | Категория товара |
| `product_name` | Название товара |
| `quantity` | Количество проданных единиц |
| `unit_price` | Цена одной единицы |
| `payment_method` | Способ оплаты |

Базовая метрика проекта: `quantity * unit_price`.

## Данные студента

- ФИО: `Бальцевич А. И., Лобзик В. А., Ерофеева В. Е.`;
- группа: `СДП-ИИ-231`;
- домен: розничные продажи.
