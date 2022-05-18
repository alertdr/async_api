import pytest
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from ..testdata.genres import Genres
from ..testdata.movies import Movies
from ..testdata.persons import Persons


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
    model = Genres
    await _fill_db(es_client, index, model)
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture(scope='module')
async def fill_db_persons(es_client: AsyncElasticsearch):
    index = 'persons'
    model = Persons
    await _fill_db(es_client, index, model)
    yield
    await es_client.indices.delete(index=index)


@pytest.fixture(autouse=True)
async def clean_redis(redis_client: Redis):
    await redis_client.flushdb(asynchronous=True)


async def _fill_db(es_client: AsyncElasticsearch, index, cls):
    if await es_client.indices.exists(index=index):
        raise ValueError(f'Elastic db contains {index} index, possibility prod version. Check db.')
    await es_client.indices.create(index=index, body=cls.mapping)
    data = [{'_index': index, '_id': item['id'], '_source': item} for item in cls.data]
    await async_bulk(es_client, data, refresh=True)
