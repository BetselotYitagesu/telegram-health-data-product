from fastapi import FastAPI
from api.endpoints import messages  # and other endpoints as created

app = FastAPI(title="Telegram Health Data Product API")

app.include_router(messages.router, prefix="/api")
