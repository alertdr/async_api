import json
import logging

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from orjson import dumps, loads

from models.base_models import BaseApiConfig

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
PAGE_SIZE = 10

logger = logging.getLogger(__name__)


class BaseService:
    index = None
    kwargs: dict = {}
    response_model = BaseApiConfig
    search_fields = []

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def _put_item_to_cache(self, id: str, obj: BaseApiConfig | list[BaseApiConfig]) -> None:
        if isinstance(obj, list):
            raw = dumps([item.json() for item in obj])
        else:
            raw = obj.json()
        logger.debug('Put to cache with id=%s', id)
        await self.redis.set(id, raw, ex=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_item_from_cache(self, id: str) -> BaseApiConfig | list[BaseApiConfig] | None:
        logger.debug('Looking in cache with id=%s', id)
        data = await self.redis.get(id)
        if not data:
            logger.info('Cached not found, go to elastic')
            return None
        logger.info('Found in cache, use data.')
        obj = loads(data)
        if isinstance(obj, list):
            return [self.response_model.parse_raw(item) for item in obj]
        return self.response_model.parse_raw(data)

    async def _get_item_from_elastic(self, id: str) -> BaseApiConfig | None:
        result = await self.elastic.search(index=self.index, body={
            "query": {
                "match": {
                    "id": id
                }
            }
        })
        if docs := result['hits']['hits']:
            logger.info('Elastic found id.')
            return self.response_model(**docs[0]['_source'])
        return None

    def create_list_id(self) -> str:
        return json.dumps(self.kwargs, sort_keys=True)

    async def _put_list_to_cache(self, items: list[BaseApiConfig]) -> None:
        id = self.create_list_id()
        await self._put_item_to_cache(id, items)

    async def _get_list_from_cache(self) -> list[BaseApiConfig] | None:
        id = self.create_list_id()
        if cached := await self._get_item_from_cache(id):
            return cached                                                   # type: ignore
        return None

    async def _get_list_from_elastic(self) -> list[BaseApiConfig]:
        result = await self.elastic.search(index='movies', body=self.body)
        docs = result['hits']['hits']
        if docs:
            logger.info('Elastic found something.')
            return [self.response_model(**doc['_source']) for doc in docs]
        logger.info('Elastic found nothing.')
        return []

    async def get_by_id(self, item_id: str) -> BaseApiConfig | None:
        if obj := await self._get_item_from_cache(item_id):
            return obj                                                      # type: ignore
        if obj := await self._get_item_from_elastic(item_id):
            await self._put_item_to_cache(obj.id, obj)
            return obj                                                      # type: ignore
        return None

    async def get_list(self, **kwargs) -> list[BaseApiConfig]:
        self.kwargs = kwargs
        self.body = self._body_formation()
        if objs := await self._get_list_from_cache():
            return objs
        if objs := await self._get_list_from_elastic():
            await self._put_list_to_cache(objs)
        return objs

    def _filter_query(self, filter: dict) -> dict:
        '''
        Функция для фильтра по полям конкретного индекса. Определяется в дочернем классе.
        '''
        return {}

    def _body_formation(self) -> dict:
        self.kwargs['index'] = self.index
        body: dict = {}
        logger.debug('Parameters set to %s', self.kwargs)
        if query := self.kwargs.get('query', None):
            body['query'] = {
                "multi_match": {
                    "query": query,
                    "fields": self.search_fields
                }
            }
        else:
            body['query'] = {'match_all': {}}
        logger.debug('Query set to %s', body['query'])
        if filter := self.kwargs.get('filter', None):
            if isinstance(filter, dict):
                body['filter'] = self._filter_query(filter)
            else:
                body['filter'] = {'id': {'values': filter}}
        if (page := self.kwargs.get('page', None)) and isinstance(page, dict):
            size = page['size'] if 'size' in page else PAGE_SIZE
            body['size'] = size
            body['from'] = ((int(page['number']) - 1) * int(size)) if 'number' in page else 0
            logger.debug('Pagination set to size %s, from item %s', body['size'], body['from'])
        if sort := self.kwargs.get('sort', None):
            order = 'desc' if sort.startswith('-') else 'asc'
            body.update({'sort': {sort.lstrip('-'): order}})
            logger.debug('Sort set to %s', body['sort'])
        return body
