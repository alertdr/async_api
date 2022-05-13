import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest as pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .config import API_URL, ELASTIC_HOST, REDIS_URL
from .testdata.film import movies_mapping


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=ELASTIC_HOST)
    if not await client.indices.exists(index='movies'):
        await client.indices.create(index='movies', body=movies_mapping)
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def redis_client():
    client = await aioredis.from_url(REDIS_URL, decode_responses=True)
    await client.flushall()
    yield client
    await client.close()


@pytest.fixture
def get_request(session):
    async def inner(path: str, params: Optional[dict] = None) -> HTTPResponse:
        url = API_URL + path
        params = params or {}
        async with session.get(url, params=params, allow_redirects=True) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
