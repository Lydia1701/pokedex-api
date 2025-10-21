from contextlib import asynccontextmanager
from fastapi import Depends
from sqlalchemy.orm import Session
from redis import asyncio as aioredis
from .db import SessionLocal
from .config import REDIS_URL

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

_redis_client: aioredis.Redis | None = None

async def get_redis() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)
    return _redis_client
