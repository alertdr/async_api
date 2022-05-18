import asyncio
from dataclasses import dataclass

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .config import ELASTIC_HOST, REDIS_URL, API_URL

CLIENT_URL = API_URL + '/api/v1'

pytest_plugins = ['app.fixtures.fill_db']


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
    client = AsyncElasticsearch(hosts=ELASTIC_HOST)
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
def get_request(http_session):
    async def inner(method: str, params: dict | None = None) -> HTTPResponse:
        params = params or {}
        url = CLIENT_URL + method
        async with http_session.get(url, params=params, allow_redirects=True) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
