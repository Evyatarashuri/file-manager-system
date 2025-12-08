import os
import redis
from typing import Optional
from app.config.logging import get_logger

logger = get_logger("redis")

_redis_client: Optional[redis.Redis] = None

def get_redis_client() -> redis.Redis:
    """Singleton Redis connection for Cloud MemoryStore + local dev"""

    global _redis_client
    if _redis_client is not None:
        return _redis_client

    REDIS_HOST = os.getenv("REDIS_HOST", None)         # Cloud MemoryStore IP
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASS = os.getenv("REDIS_PASSWORD", None)     # Usually None on MemoryStore

    if not REDIS_HOST:
        raise RuntimeError("REDIS_HOST missing! (Must be MemoryStore private IP)")

    try:
        _redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASS,
            decode_responses=True,      # return str instead of bytes
            socket_keepalive=True,
            socket_timeout=3,
        )
        _redis_client.ping()
        logger.info(f"Connected → Redis {REDIS_HOST}:{REDIS_PORT}")
        return _redis_client

    except Exception as e:
        logger.error(f"Failed connecting to Redis {REDIS_HOST}:{REDIS_PORT}", exc_info=True)
        raise
