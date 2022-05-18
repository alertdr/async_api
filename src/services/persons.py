import logging
from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person

from .basic import BaseService, AsyncCacheStorage, AsyncFullTextSearch

logger = logging.getLogger(__name__)


class PersonService(BaseService):
    index = 'persons'
    response_model = Person
    search_fields = [
        'name',
    ]


@lru_cache()
def get_person_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        searcher: AsyncFullTextSearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(cache, searcher)
