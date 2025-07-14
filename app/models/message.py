from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessageBase(BaseModel):
    message_id: int
    date: datetime
    channel: str
    sender: Optional[str]
    text: Optional[str]
    has_media: bool
    media_file_path: Optional[str]


class MessageResponse(MessageBase):
    pass
