import pytest
from elasticsearch import helpers

from ..testdata.film import single_film, single_film2, expected_films
from ..testdata.person import *

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'path, expected, upload_data, status_code',
    [
        ['/api/v1/persons/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', expected_single_person, [single_person], 200],
        ['/api/v1/persons/test', {"detail": "nothing found"}, [], 404]
    ]
)
async def test_search_by_id(es_client, get_request, path, expected, upload_data, status_code):
    await helpers.async_bulk(es_client, upload_data, refresh='wait_for')
    response = await get_request(path=path)

    assert response.status == status_code
    assert response.body == expected


async def test_search_persons(es_client, get_request):
    await helpers.async_bulk(es_client, [single_person2, single_person], refresh='wait_for')
    response = await get_request(path='/api/v1/persons/')

    assert response.status == 200
    assert len(response.body) == 2
    assert response.body == expected_persons


@pytest.mark.parametrize(
    'path, expected, upload_data, status_code, redis_key',
    [
        ['/api/v1/persons/5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', expected_cache, [single_person2], 200,
         '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1'],
        ['/api/v1/persons/test', None, [], 404, '']
    ]
)
async def test_redis_cache(redis_client, es_client, get_request, path, expected, upload_data, status_code, redis_key):
    await helpers.async_bulk(es_client, upload_data, refresh='wait_for')
    response = await get_request(path=path)
    redis_cache = await redis_client.get('persons::{"item_id": "%s"}' % redis_key)

    assert response.status == status_code
    assert redis_cache == expected


@pytest.mark.parametrize(
    'path, expected, upload_data, status_code, content_length',
    [
        ['/api/v1/persons/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a/film/', expected_films, [single_film, single_film2],
         200, 2],
        ['/api/v1/persons/test/film/', [], [], 200, 0]
    ]
)
async def test_search_films_by_person(es_client, get_request, path, expected, upload_data, status_code, content_length):
    await helpers.async_bulk(es_client, upload_data, refresh='wait_for')
    response = await get_request(path=path)

    assert response.status == status_code
    assert len(response.body) == content_length
    assert response.body == expected
