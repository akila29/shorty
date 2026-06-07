import logging

import redis.asyncio as aioredis

from app.config import settings

logger = logging.getLogger(__name__)

_redis: aioredis.Redis | None = None


async def init_cache() -> None:
    global _redis
    _redis = aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )


async def close_cache() -> None:
    if _redis:
        await _redis.aclose()


async def cache_get(key: str) -> str | None:
    try:
        return await _redis.get(key)  # type: ignore[union-attr]
    except Exception:
        logger.warning("Redis get failed for key=%s", key)
        return None


async def cache_set(key: str, value: str, ttl: int = settings.redis_ttl_seconds) -> None:
    try:
        await _redis.set(key, value, ex=ttl)  # type: ignore[union-attr]
    except Exception:
        logger.warning("Redis set failed for key=%s", key)
