from redis import Redis

from app.config import config
from .client import RedisClient


async def get_redis_client() -> RedisClient:
    return RedisClient().from_url(config.redis.dsn, single_connection_client=True)
