from fastapi import FastAPI, HTTPException, Query
from typing import List
from . import crud
from .schemas import TopProduct, ChannelActivity, MessageSearchResult


app = FastAPI(title="Telegram Medical Analytics API")


@app.get(
    "/api/reports/top-products",
    response_model=List[TopProduct],
)
def api_top_products(limit: int = Query(10, ge=1, le=100)):
    data = crud.get_top_products(limit)
    return [
        {"product_name": row[0], "mention_count": row[1]}
        for row in data
    ]


@app.get(
    "/api/channels/{channel_name}/activity",
    response_model=List[ChannelActivity],
)
def api_channel_activity(channel_name: str):
    data = crud.get_channel_activity(channel_name)
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Channel not found or no data",
        )
    return [
        {"channel_name": row[0], "daily_post_count": row[2]}
        for row in data
    ]


@app.get(
    "/api/search/messages",
    response_model=List[MessageSearchResult],
)
def api_search_messages(query: str = Query(..., min_length=3)):
    data = crud.search_messages(query)
    if not data:
        raise HTTPException(
            status_code=404,
            detail="No messages found for query",
        )
    return [
        {
            "message_id": row[0],
            "channel_name": row[1],
            "message_text": row[2],
            "date_posted": row[3].isoformat() if row[3] else None,
        }
        for row in data
    ]
