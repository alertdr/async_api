import pytest
from elasticsearch import helpers

from ..testdata.film import single_film, single_film2, expected_films
from ..testdata.person import *


@pytest.mark.asyncio
async def test_search_by_id(es_client, get_request):
    await helpers.async_bulk(es_client, [single_person])

    response = await get_request(path='/api/v1/persons/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a')

    assert response.status == 200
    assert response.body == expected_single_person


@pytest.mark.asyncio
async def test_search_persons(es_client, get_request):
    await helpers.async_bulk(es_client, [single_person2])

    response = await get_request(path='/api/v1/persons/')

    assert response.status == 200
    assert len(response.body) == 2
    assert response.body == expected_persons


@pytest.mark.asyncio
async def test_redis_cache(redis_client, es_client, get_request):
    await helpers.async_bulk(es_client, [single_person2])
    response = await get_request(path='/api/v1/persons/5b4bf1bc-3397-4e83-9b17-8b10c6544ed1')
    redis_cache = await redis_client.get('persons::{"item_id": "5b4bf1bc-3397-4e83-9b17-8b10c6544ed1"}')

    assert response.status == 200
    assert redis_cache
    assert redis_cache == expected_cache


@pytest.mark.asyncio
async def test_search_films_by_person(es_client, get_request):
    await helpers.async_bulk(es_client, [single_film, single_film2])

    response = await get_request(path='/api/v1/persons/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a/film/')

    assert response.status == 200
    assert len(response.body) == 2
    assert response.body == expected_films
