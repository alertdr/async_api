import pytest
from elasticsearch import helpers

from ..testdata.film import Movies
from ..testdata.person import Persons

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'path, expected, upload_data, status_code',
    [
        ['persons/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a', Persons.expected_person1, [Persons.person1], 200],
        ['persons/test', {"detail": "nothing found"}, [], 404]
    ]
)
async def test_search_by_id(es_client, get_request, path, expected, upload_data, status_code):
    await helpers.async_bulk(es_client, upload_data, refresh='wait_for')
    response = await get_request(path=path)
    print(response.body)
    assert response.status == status_code
    assert response.body == expected


async def test_search_persons(es_client, get_request):
    await helpers.async_bulk(es_client, [Persons.person2, Persons.person1], refresh='wait_for')
    response = await get_request(path='persons/')

    assert response.status == 200
    assert len(response.body) == 2
    print(response.body)
    assert response.body == Persons.expected_persons


@pytest.mark.parametrize(
    'path, expected, upload_data, status_code, redis_key',
    [
        ['persons/5b4bf1bc-3397-4e83-9b17-8b10c6544ed1', Persons.expected_cache, [Persons.person2], 200,
         '5b4bf1bc-3397-4e83-9b17-8b10c6544ed1'],
        ['persons/test', None, [], 404, '']
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
        ['persons/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a/film/', Movies.expected_films,
         [Movies.film1, Movies.film2], 200, 2],
        ['persons/test/film/', [], [], 200, 0]
    ]
)
async def test_search_films_by_person(es_client, get_request, path, expected, upload_data, status_code, content_length):
    await helpers.async_bulk(es_client, upload_data, refresh='wait_for')
    response = await get_request(path=path)

    assert response.status == status_code
    assert len(response.body) == content_length
    assert response.body == expected
