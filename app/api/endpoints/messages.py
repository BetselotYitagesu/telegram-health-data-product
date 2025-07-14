from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db.session import get_db
from db.crud import get_messages
from models.message import MessageResponse

router = APIRouter()

@router.get("/messages/", response_model=List[MessageResponse])
async def read_messages(limit: int = 100, db: AsyncSession = Depends(get_db)):
    messages = await get_messages(db, limit)
    return messages
