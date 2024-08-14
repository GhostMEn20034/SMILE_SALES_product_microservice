from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.config.settings import settings
from .cache.key_builder import request_key_builder


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.redis_cache_url, decode_responses=False)
    try:
        await redis.ping()  # Check if Redis is reachable
        print("Successfully connected to Redis")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
    FastAPICache.init(RedisBackend(redis), prefix="product_data", key_builder=request_key_builder)
    yield
