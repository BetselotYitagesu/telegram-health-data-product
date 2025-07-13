import os
import psycopg2
from dotenv import load_dotenv

# Load .env file
load_dotenv()


def test_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", 5432),
        )
        print("✅ Connection to PostgreSQL was successful!")
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    test_connection()
