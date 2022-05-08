from dataclasses import dataclass
from elasticsearch.helpers import async_bulk
import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy
import asyncio
from redis import Redis

from testdata.movies_data import Movies

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


async def check_db_index_is_clean(es_client: AsyncElasticsearch, index: str):
    if await es_client.indices.exists(index=index):
        raise ValueError(f'Elastic db contains {index} index, possibility prod version. Check db.')


@pytest.fixture(scope='session')
async def fill_db(es_client: AsyncElasticsearch):
    index = 'movies'
    await check_db_index_is_clean(es_client, index)
    if not await es_client.indices.exists(index=index):
        await es_client.indices.create(index=index, body=Movies.mapping)
    data = [{'_index': 'movies', '_id': item['id'], '_source': item} for item in Movies.data]
    await async_bulk(es_client, data)
    while (response := await es_client.search(index=index)) and response['hits']['total']['value'] < len(Movies.data):
        print('Ждем данные в базе...')
        await asyncio.sleep(.1)
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture()
def clean_redis(redis_client):
    redis_client.flushdb()
