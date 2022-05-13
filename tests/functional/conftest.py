import asyncio
from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from multidict import CIMultiDictProxy
from testdata.genres_data import Genre
from testdata.movies_data import Movies

from redis import Redis

ES_HOST = '127.0.0.1:9200'
REDIS_HOST = '127.0.0.1:6379'
CLIENT_URL = 'http://127.0.0.1:8000/api/v1'
REDIS_URL = f'redis://{REDIS_HOST}'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=ES_HOST)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def redis_client():
    client = await aioredis.from_url(REDIS_URL, decode_responses=True)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def http_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(http_session):
    async def inner(method: str, params: dict | None = None) -> HTTPResponse:
        params = params or {}
        url = CLIENT_URL + method
        async with http_session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner


@pytest.fixture(scope='module')
async def fill_db_movies(es_client: AsyncElasticsearch):
    index = 'movies'
    model = Movies
    await _fill_db(es_client, index, model)
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture(scope='module')
async def fill_db_genres(es_client: AsyncElasticsearch):
    index = 'genres'
    model = Genre
    await _fill_db(es_client, index, model)
    yield
    await es_client.indices.delete(index=index)


async def _fill_db(es_client: AsyncElasticsearch, index, cls):
    if await es_client.indices.exists(index=index):
        raise ValueError(f'Elastic db contains {index} index, possibility prod version. Check db.')
    await es_client.indices.create(index=index, body=cls.mapping)
    data = [{'_index': index, '_id': item['id'], '_source': item} for item in cls.data]
    await async_bulk(es_client, data, refresh=True)


@pytest.fixture(autouse=True)
async def clean_redis(redis_client: Redis):
    await redis_client.flushdb(asynchronous=True)
