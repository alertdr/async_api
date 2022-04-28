import json
import logging

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from orjson import dumps, loads

from models.base_models import BaseApiConfig

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5
PAGE_SIZE = 10

logger = logging.getLogger(__name__)


class BaseService:
    index = ''
    kwargs: dict = {}
    response_model = BaseApiConfig
    search_fields = []

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def _put_to_cache(self, obj: BaseApiConfig | list[BaseApiConfig]) -> None:
        if isinstance(obj, list):
            raw = dumps([item.json() for item in obj])
        else:
            raw = obj.json()
        key = self.create_redis_key()
        logger.debug('Put to cache with key=%s', key)
        await self.redis.set(key, raw, ex=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_from_cache(self) -> BaseApiConfig | list[BaseApiConfig] | None:
        key = self.create_redis_key()
        logger.debug('Looking in cache with key=%s', key)
        data = await self.redis.get(key)
        if not data:
            logger.info('Cached not found, go to elastic')
            return None
        logger.info('Found in cache, use data.')
        obj = loads(data)
        if isinstance(obj, list):
            return [self.response_model.parse_raw(item) for item in obj]
        return self.response_model.parse_raw(data)

    def create_redis_key(self) -> str:
        key: str = f'{self.index}::'
        return key + json.dumps(self.kwargs)

    async def _get_from_elastic(self, body) -> list[BaseApiConfig] | BaseApiConfig | None:
        result = await self.elastic.search(index=self.index, body=body)
        docs = result['hits']['hits']
        match result['hits']['total']['value']:
            case 0:
                logger.info('Elastic found nothing.')
                return None
            case 1:
                logger.info('Elastic found one.')
                return self.response_model(**docs[0]['_source'])
            case _:
                logger.info('Elastic found many.')
                return [self.response_model(**doc['_source']) for doc in docs]

    async def get_by_id(self, item_id: str) -> BaseApiConfig | None:
        self.kwargs = {'item_id': item_id}
        if obj := await self._get_from_cache():
            return obj                                                      # type: ignore
        body = {"query": {"match": {"id": item_id}}}
        if obj := await self._get_from_elastic(body):
            await self._put_to_cache(obj)
            return obj                                                      # type: ignore
        return None

    async def get_list(self, **kwargs) -> list[BaseApiConfig]:
        self.kwargs = kwargs
        body = self._body_formation()
        if objs := await self._get_from_cache():
            return objs                                                     # type: ignore
        if objs := await self._get_from_elastic(body):
            await self._put_to_cache(objs)
        return objs                                                         # type: ignore

    def _filter_query(self, filter: dict) -> dict:
        '''
        Функция для фильтра по полям конкретного индекса. Определяется в дочернем классе.
        '''
        return {}

    def _body_formation(self) -> dict:
        body: dict = {}
        logger.debug('Parameters set to %s', self.kwargs)
        if filter := self.kwargs.get('filter', None):
            if isinstance(filter, dict):
                filter = self._filter_query(filter)
            else:
                filter = {'term': {'id': filter}}
            body['query'] = {'bool': {'filter': filter}}
            logger.debug('Filter set to %s', body['query'])
        elif query := self.kwargs.get('query', None):
            body['query'] = {
                "multi_match": {
                    "query": query,
                    "fields": self.search_fields
                }
            }
            logger.debug('Query set to %s', body['query'])
        if (page := self.kwargs.get('page', None)) and isinstance(page, dict):
            body['size'] = page['size']
            body['from'] = (page['number'] - 1) * page['size']
            logger.debug('Pagination set to size %s, from item %s', body['size'], body['from'])
        if sort := self.kwargs.get('sort', None):
            order = 'desc' if sort.startswith('-') else 'asc'
            body.update({'sort': {sort.lstrip('-'): order}})
            logger.debug('Sort set to %s', body['sort'])
        return body
