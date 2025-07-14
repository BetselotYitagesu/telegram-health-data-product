import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS raw.image_detections (
        message_id INTEGER,
        class_name TEXT,
        confidence FLOAT,
        image_file TEXT
    );
""")
conn.commit()

df = pd.read_csv("data/processed/image_detections.csv")

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO raw.image_detections (message_id, class_name, confidence, 
                image_file)
        VALUES (%s, %s, %s, %s)
    """, (row.message_id, row.class_name, row.confidence, row.image_file))

conn.commit()
print("✅ Image detections loaded into Postgres.")
