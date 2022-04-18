from typing import Optional

import aioredis
from aioredis import Redis

from core.config import REDIS_URL

redis: Optional[Redis] = None


async def get_redis() -> Redis:
     return await aioredis.from_url(REDIS_URL, max_connections=20, decode_responses=True)
