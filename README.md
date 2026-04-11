# Open Data AI Analytics: Docker Lab

Проєкт реалізує повний контейнеризований конвеєр для набору відкритих даних про реєстрацію транспортних засобів в Україні. Усі модулі винесені в окремі сервіси з власними `Dockerfile`, а спільний запуск виконується через `docker compose up --build`.

## Структура проєкту
- `data_load/` імпортує CSV у SQLite.
- `data_quality_analysis/` обчислює пропуски, дублікати та перевірки коректності значень.
- `data_research/` створює базовий статистичний звіт.
- `visualization/` генерує PNG-графіки для веб-інтерфейсу.
- `web/` запускає FastAPI + Jinja інтерфейс для перегляду результатів.
- `src/common/` містить спільні модулі конфігурації, роботи з БД, звітів і графіків.
- `data/raw/` містить вхідний CSV.
- `runtime/` містить SQLite базу даних.
- `reports/` містить JSON-звіти та графіки.

## Джерело даних
- Набір: [Реєстр транспортних засобів та їх власників](https://data.gov.ua/dataset/0ffd8b75-0628-48cc-952a-9302f9799ec0)
- ZIP-архів: [download](https://data.gov.ua/dataset/0ffd8b75-0628-48cc-952a-9302f9799ec0/resource/bef7b47b-7963-44b5-88a8-f84241137b5b/download/reestrtz2022.zip)
- Основний CSV: `data/raw/tz_opendata_z01012022_po01032022.csv`

## Запуск через Docker
1. Переконайтеся, що Docker запущено.
2. За потреби скопіюйте `.env.example` у `.env` і змініть параметри.
3. Запустіть систему:

```bash
docker compose up --build
```

4. Відкрийте веб-інтерфейс:

```text
http://localhost:8000
```

## Що створюють сервіси
- `data_load` створює `runtime/transport_registry.sqlite3` і таблицю `transport_data`.
- `data_quality_analysis` створює `reports/data_quality_report.json`.
- `data_research` створює `reports/data_research_report.json`.
- `visualization` створює графіки в `reports/plots/` і `reports/visualization_manifest.json`.
- `web` показує зведену сторінку з усіма результатами через браузер.

## Локальна перевірка без Docker
Встановіть залежності:

```bash
pip install -r requirements.txt
```

Запустіть модулі по черзі:

```bash
python data_load/app.py
python data_quality_analysis/app.py
python data_research/app.py
python visualization/app.py
uvicorn web.app:app --host 0.0.0.0 --port 8000
```
