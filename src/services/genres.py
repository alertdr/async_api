import logging
from functools import lru_cache

from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from .basic import BaseService, AsyncCacheStorage, AsyncFullTextSearch

logger = logging.getLogger(__name__)


class GenreService(BaseService):
    index = 'genres'
    response_model = Genre
    search_fields = [
        'name',
        'description'
    ]


@lru_cache()
def get_genre_service(
        cache: AsyncCacheStorage = Depends(get_redis),
        searcher: AsyncFullTextSearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache, searcher)
