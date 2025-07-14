import os
import json
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT")
)
cursor = conn.cursor()

# Directory where JSON files are stored
data_dir = Path("data/raw/telegram_messages")

for date_folder in data_dir.iterdir():
    for json_file in date_folder.glob("*.json"):
        channel_name = json_file.stem
        with open(json_file, "r", encoding="utf-8") as f:
            messages = json.load(f)
            for msg in messages:
                message_id = msg.get("id")
                date = msg.get("date")
                channel = channel_name  # Use file name as fallback
                sender = str(msg.get("sender_id"))  # Convert to str
                text = msg.get("message")
                has_media = msg.get("has_media", False)
                media_file_path = msg.get("image_path")

                cursor.execute("""
                    INSERT INTO raw.telegram_messages (
                        message_id, date, channel, sender, text, has_media, 
                               media_file_path
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (message_id) DO NOTHING
                """, (
                    message_id,
                    date,
                    channel,
                    sender,
                    text,
                    has_media,
                    media_file_path
                ))

conn.commit()
cursor.close()
conn.close()
print("✅ Raw messages loaded successfully.")
