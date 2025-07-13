import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Get credentials
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    raise ValueError("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH in .env")

API_ID = int(API_ID)

# Create Telegram client
client = TelegramClient("anon", API_ID, API_HASH)

# Main scraping function
async def scrape_channel(channel_username, limit=100):
    await client.start()
    print(f"🔍 Scraping {channel_username}...")

    # Resolve channel entity
    entity = await client.get_entity(channel_username)

    # Fetch message history
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

    # Prepare folders
    date_str = datetime.now().strftime("%Y-%m-%d")
    message_folder = os.path.join("data", "raw", "telegram_messages", date_str)
    image_folder = os.path.join("data", "raw", "images", date_str)
    os.makedirs(message_folder, exist_ok=True)
    os.makedirs(image_folder, exist_ok=True)

    # Prepare message list
    messages = []

    # Loop through each message
    for msg in history.messages:
        msg_data = {
            "id": msg.id,
            "date": str(msg.date),
            "message": msg.message,
            "sender_id": msg.sender_id,
            "has_media": msg.media is not None
        }

        # Download image if exists
        if msg.media and isinstance(msg.media, MessageMediaPhoto):
            image_path = os.path.join(image_folder, f"{channel_username[1:]}_{msg.id}.jpg")
            await client.download_media(msg, file=image_path)
            msg_data["image_path"] = image_path
            print(f"📸 Image saved: {image_path}")

        messages.append(msg_data)

    # Save messages to JSON
    output_path = os.path.join(message_folder, f"{channel_username[1:]}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

    print(
        f"✅ Saved {len(messages)} messages from "
        f"{channel_username} to {output_path}"
)

# Run on multiple channels
if __name__ == "__main__":
    channels = [
        "lobelia4cosmetics",
        "tikvahpharma",
        # Add more if needed, e.g., "chemedchannel"
    ]
    for channel in channels:
        asyncio.run(scrape_channel(channel, limit=100))
