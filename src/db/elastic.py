from typing import Optional

from elasticsearch import AsyncElasticsearch

from core.config import ELASTIC_HOST

es: Optional[AsyncElasticsearch] = None


async def get_elastic() -> AsyncElasticsearch:
    return AsyncElasticsearch(ELASTIC_HOST)
