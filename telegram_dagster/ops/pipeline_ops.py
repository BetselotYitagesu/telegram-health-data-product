# telegram_dagster/ops/pipeline_ops.py
from dagster import op
import subprocess


@op
def scrape_telegram_data():
    subprocess.run(["python", "src/telegram_scraper.py"], check=True)


@op
def load_raw_to_postgres():
    subprocess.run(["python", "src/load_raw_to_postgres.py"], check=True)


@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run", "--project-dir", "telegram_dbt"], check=True)


@op
def run_yolo_enrichment():
    subprocess.run(["python", "src/yolo_enrichment.py"], check=True)
