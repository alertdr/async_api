import logging

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from models.base_models import BaseApiConfig
from orjson import dumps, loads

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут
PAGE_SIZE = 10

logger = logging.getLogger(__name__)


class BaseService:
    index = None
    kwargs = {}
    response_model = BaseApiConfig

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def _put_item_to_cache(self, id: str, obj: BaseApiConfig | list[BaseApiConfig]) -> None:
        if isinstance(obj, list):
            raw = dumps([item.json() for item in obj])
        else:
            raw = obj.json()
        await self.redis.set(id, raw, ex=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _get_item_from_cache(self, id: str) -> BaseApiConfig | list[BaseApiConfig] | None:
        data = await self.redis.get(id)
        if not data:
            return None
        if isinstance(data, list):
            return [self.response_model.parse_raw(raw) for raw in data]
        return self.response_model.parse_raw(data)

    async def _get_item_from_elastic(self, id: str) -> BaseApiConfig | None:
        result = await self.elastic.search(index=self.index, body={
            "query": {
                "match": {
                    "id": id
                }
            }
        })
        logger.debug('Elastic send %s', result)
        if docs := result['hits']['hits']:
            return self.response_model(**docs[0]['_source'])
        return None

    def create_list_id(self) -> str:
        kwargs = self.kwargs
        kwargs['index'] = self.index
        return json.dumps(kwargs, sort_keys=True)

    async def _put_list_to_cache(self, items: list[BaseApiConfig]) -> None:
        id = self.create_list_id()
        await self._put_item_to_cache(id, items)

    async def _get_list_from_cache(self) -> list[BaseApiConfig] | None:
        id = self.create_list_id()
        if cached := await self._get_item_from_cache(id):
            logger.debug('Received from redis - %s', cached)
            return cached                                                   # type: ignore
        return None

    async def _get_list_from_elastic(self) -> list[BaseApiConfig]:
        body = self._body_formation()
        result = await self.elastic.search(index='movies', body=body)
        docs = result['hits']['hits']
        return [self.response_model(**doc['_source']) for doc in docs]

    async def get_by_id(self, item_id: str) -> BaseApiConfig | None:
        if obj := (await self._get_item_from_cache(item_id) or await self._get_item_from_elastic(item_id)):
            await self._put_item_to_cache(obj.id, obj)
            return obj                                                      # type: ignore
        return None

    async def get_list(self, **kwargs) -> list[BaseApiConfig]:
        self.kwargs = kwargs
        if objs := await self._get_list_from_cache() or await self._get_list_from_elastic():
            await self._put_list_to_cache(objs)
        logger.debug('List recieved - %s', objs)
        return objs

    def _body_formation(self) -> dict:
        kwargs = self.kwargs
        body: dict = {}
        logger.debug('Parameters set to %s', kwargs)
        if query := kwargs.get('query', None):
            body.update({
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            "title",
                            "description"
                        ]
                    }
                }
            })
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
'' dict убираем на json''