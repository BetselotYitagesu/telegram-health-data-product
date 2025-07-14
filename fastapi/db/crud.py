from sqlalchemy.future import select
from models.message import MessageResponse
from db.models import TelegramMessage  # Your SQLAlchemy ORM model


async def get_messages(session, limit=100):
    result = await session.execute(select(TelegramMessage).limit(limit))
    messages = result.scalars().all()
    return messages
