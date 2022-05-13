import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest as pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .config import API_URL, ELASTIC_HOST, REDIS_URL
from .testdata.film import Movies
from .testdata.genre import Genres
from .testdata.person import Persons

INDICES = {'persons': Persons, 'genres': Genres, 'movies': Movies}
URL = API_URL + '/api/v1/'


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
    await create_indices(es=client)
    yield client
    await client.indices.delete(index=list(INDICES.keys()))
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
        url = URL + path
        params = params or {}
        async with session.get(url, params=params, allow_redirects=True) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


async def create_indices(es: AsyncElasticsearch):
    for index_name, model in INDICES.items():
        if not await es.indices.exists(index=index_name):
            await es.indices.create(index=index_name, body=model.mapping)
