import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from dotenv import load_dotenv

load_dotenv()

# Load credentials
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("anon", API_ID, API_HASH)


async def scrape_channel(channel_username, limit=100):
    await client.start()
    entity = await client.get_entity(channel_username)

    history = await client(GetHistoryRequest(
        peer=entity,
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    messages = []
    for msg in history.messages:
        messages.append({
            "id": msg.id,
            "date": str(msg.date),
            "message": msg.message,
            "sender_id": msg.sender_id,
            "has_media": msg.media is not None
        })

    # Save to data lake
    date_str = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(f"data/raw/telegram_messages/{date_str}", exist_ok=True)

    # Build output path
    folder = f"data/raw/telegram_messages/{date_str}"
    filename = f"{channel_username[1:]}.json"
    output_path = os.path.join(folder, filename)

    # Make sure folder exists
    os.makedirs(folder, exist_ok=True)

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(messages)} messages from {channel_username}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(scrape_channel("lobelia4cosmetics", limit=100))
