# Telegram Health Data Product 🚀

An end-to-end data platform built to analyze Ethiopian medical product trends from public Telegram channels. This project extracts, stores, transforms, and prepares data for analytical APIs and enrichment using YOLOv8.

---

## 📦 Project Structure

telegram-health-data-product/
├── data/ # Raw scraped Telegram data (JSON, images)
│ └── raw/
├── docker/ # (Optional Docker setup)
├── dbt/ # dbt transformation scripts
├── fastapi/ # FastAPI analytics endpoints (Task 4)
├── notebooks/ # Exploration or prototyping
├── dags/ # Dagster orchestration logic (Task 5)
├── logs/ # Logging and error tracking
├── src/
│ ├── telegram_scraper.py # Scrapes Telegram messages and media
│ └── load_raw_to_postgres.py # Loads raw JSON to PostgreSQL
├── .env # Environment variables (ignored by Git)
├── .gitignore
├── requirements.txt
├── README.md

telegram-health-data-product/
├── data/ # Raw scraped Telegram data (JSON, images)
│ └── raw/
├── docker/ # (Optional Docker setup)
├── dbt/ # dbt transformation scripts
├── fastapi/ # FastAPI analytics endpoints (Task 4)
├── notebooks/ # Exploration or prototyping
├── dags/ # Dagster orchestration logic (Task 5)
├── logs/ # Logging and error tracking
├── src/
│ ├── telegram_scraper.py # Scrapes Telegram messages and media
│ └── load_raw_to_postgres.py # Loads raw JSON to PostgreSQL
├── .env # Environment variables (ignored by Git)
├── .gitignore
├── requirements.txt
├── README.md


---

## ✅ Tasks Completed

### Task 0: Project Setup & Environment
- Initialized Git repository
- Added `.env` for secrets and `.gitignore`
- Created folder structure for raw data, dbt, FastAPI, Dagster, and logs
- Installed required dependencies in `requirements.txt`
- Set up PostgreSQL database manually (non-Docker)

### Task 1: Data Scraping & Collection
- Used Telethon to scrape messages from public Telegram channels
- Saved data to structured JSON files under `data/raw/telegram_messages/YYYY-MM-DD/`
- Downloaded images from messages with media and saved them to `data/raw/images/`
- Implemented logging and Flake8-compatible formatting

### Task 2: Data Modeling & Transformation (dbt)
- Set up `telegram_dbt` project
- Configured `profiles.yml` for PostgreSQL connection
- Loaded raw Telegram JSON data into `raw.telegram_messages` table
- Built dbt staging and fact models:
  - `stg_telegram_messages`
  - `fct_messages`
- Ran successful dbt builds with valid outputs
- Schema includes message length and image flag for analysis

---

## 🔧 Requirements

- Python 3.10+
- PostgreSQL 15+
- [Telethon](https://docs.telethon.dev/)
- dbt-core (`pip install dbt-postgres`)
- psycopg2

---

## ⚙️ Run Instructions

### Step 1: Scrape Telegram
```bash
python src/telegram_scraper.py

Step 2: Load to PostgreSQL

python src/load_raw_to_postgres.py

Step 3: Run dbt transformations

cd telegram_dbt
dbt run


📌 Next Steps

    Task 3: Enrich data using YOLOv8 object detection on images

    Task 4: Build FastAPI endpoints to expose insights

    Task 5: Orchestrate with Dagster