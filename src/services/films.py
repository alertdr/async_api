import logging
from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.film import Film

logger = logging.getLogger(__name__)

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
PAGE_SIZE = 10

class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic


class FilmDetailService(FilmService):
    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        try:
            doc = await self.elastic.get('movies', film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS)


class FilmListService(FilmService):
    async def get_film_list(self, **kwargs) -> list[Film]:
        film_list: list[Film] = []
        if film_list := await self._get_film_list_from_cache(**kwargs):
            return film_list
        if film_list := await self._get_film_list_from_elastic(**kwargs):
            await self._put_film_list_to_cache(film_list, **kwargs)
        return film_list

    async def _get_film_list_from_cache(self, **kwargs) -> list[Film]:
        return []

    async def _get_film_list_from_elastic(self, **kwargs) -> list[Film]:
        body = self._body_formation(**kwargs)
        result = await self.elastic.search(index='movies', body=body)
        docs = result['hits']['hits']
        return [Film(**doc['_source']) for doc in docs]

    def _body_formation(self, **kwargs) -> dict:
        body: dict = {}
        logger.debug('Parameters set to %s', kwargs)
        if (page := kwargs.get('page', None)) and isinstance(page, dict):
            page['size'] = page['size'] if 'size' in page else PAGE_SIZE
            body['size'] = page['size']
            body['from'] = ((int(page['number']) - 1) * int(page['size'])) if 'number' in page else 0
            logger.debug('Pagination set to size %s, from item %s', body['size'], body['from'])
        if (filter := kwargs.get('filter', None)) and isinstance(filter, dict):
            for key, value in filter.items():
                body.update({
                    'query': {
                        'nested': {
                            'path': key,
                            'query': {
                                'bool': {
                                    'must': {
                                        'match': {key + '.id': value}
                                    }
                                }
                            }
                        }
                    }
                })
            logger.debug('Filter set to %s', body['query'])
        if sort := kwargs.get('sort', None):
            order = 'desc' if sort.startswith('-') else 'asc'
            body.update({'sort': {sort.lstrip('-'): order}})
            logger.debug('Sort set to %s', body['sort'])
        return body

    async def _put_film_list_to_cache(self, film_list, **kwargs) -> None:
        pass


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmDetailService(redis, elastic)


@lru_cache()
def get_film_list_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmListService(redis, elastic)
