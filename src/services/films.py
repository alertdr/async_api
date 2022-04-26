import logging
from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film

from .basic import BaseService

logger = logging.getLogger(__name__)


class FilmService(BaseService):
    index = 'movies'
    response_model = Film
    search_fields = [
        "title",
        "description"
    ]

    def _filter_query(self, filter):
        if person_id := filter.pop('person', None):
            filter.update({'actors': person_id, 'writers': person_id, 'directors': person_id})
        nested = []
        for key, value in filter.items():
            nested.append({
                "nested": {
                    "path": key,
                    "query": {
                        "term": {
                            key + ".id": value
                        }
                    }
                }
            })
        return {
            "bool": {
                "should": nested
            }
        }


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
