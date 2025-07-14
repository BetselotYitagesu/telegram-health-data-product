from pydantic import BaseModel


class TopProduct(BaseModel):
    product_name: str
    mention_count: int


class ChannelActivity(BaseModel):
    channel_name: str
    daily_post_count: int


class MessageSearchResult(BaseModel):
    message_id: int
    channel_name: str
    message_text: str
    date_posted: str  # ISO format
