from typing import Any

import pytest
from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from ..testdata.movies import Movies
from ..testdata.persons import Persons

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize('query, page_number, page_size, expected_status, expected_body, cache_size', [
    ('Harrison', 1, 10, 200, [Persons.expected[1]], 1),
    ('Harrison', 1, -1, 422, Persons.errors['not_gt_size'], 0),
    ('Harrison Fart', 1, 10, 200, [Persons.expected[1]], 1),
    ('Immanuel Cant', 1, 10, 200, [Persons.expected[2], Persons.expected[3]], 1),
    ('Immanuel Cont', 2, 1, 200, [Persons.expected[3]], 1),
    ('1337', 1, 1, 200, [], 0),
    ('13', 0, 1, 422, Persons.errors['not_gt_number'], 0),
    ('14', 1, 'q', 422, Persons.errors['int_size'], 0),
    (1337, 1, 1, 200, [], 0)
])
async def test_person_search(
        fill_db_persons, redis_client: Redis, get_request, query: str | int, page_number: int | str,
        page_size: int | str, expected_status: int, expected_body: dict | list, cache_size: int
):
    response = await get_request(f'/persons/search?query={query}&page[number]={page_number}&page[size]={page_size}')

    assert response.status == expected_status
    assert response.body == expected_body
    assert await redis_client.dbsize() == cache_size


@pytest.mark.parametrize('uuid', [item['id'] for item in Persons.data])
async def test_get_film_by_person(fill_db_persons, fill_db_movies, get_request, uuid: str):
    response = await get_request(f'/persons/{uuid}/film/')
    expected = Movies.expected_short()

    assert response.status == 200
    for film in response.body:
        assert film in expected


@pytest.mark.parametrize('page_number', [1, 2])
async def test_persons_pagination(fill_db_persons, get_request, page_number: int):
    page_size = 1
    response = await get_request(f'/persons?page[number]={page_number}&page[size]={page_size}')
    expected = Persons.expected.copy()
    portion = page_size * (page_number - 1)
    expected = expected[portion: portion + page_size]

    assert response.status == 200
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.parametrize('uuid', [item['id'] for item in Persons.data])
async def test_person_id(fill_db_persons, get_request, uuid: str):
    response = await get_request(f'/persons/{uuid}')

    assert response.status == 200
    assert len(response.body) == 6
    assert response.body in Persons.expected.copy()


@pytest.mark.parametrize('page_number, size', [(0, 1), (1, 0), (-1, 1), (1, -1), ('qq', 1), (1, 'eq')])
async def test_wrong_parameters(fill_db_persons, get_request, page_number: int | str, size: int | str):
    response = await get_request(f'/persons?page[number]={page_number}&page[size]={size}')

    assert response.status == 422


async def test_wrong_person_id(fill_db_persons, get_request):
    response = await get_request('/persons/1337')

    assert response.status == 404


@pytest.mark.parametrize('uuid', [Persons.data[0]['id']])
async def test_redis(fill_db_persons, redis_client: Redis, es_client: AsyncElasticsearch, get_request, uuid: str):
    expected = Persons.expected[0]

    assert await redis_client.dbsize() == 0

    response = await get_request(f'/persons/{uuid}')

    assert response.status == 200
    assert await redis_client.dbsize() == 1

    await es_client.update('persons', uuid, body={'doc': {'name': 'abc'}}, refresh=True)
    response = await get_request(f'/persons/{uuid}')

    assert response.status == 200
    assert response.body == expected

    await redis_client.flushdb(asynchronous=True)
    response = await get_request(f'/persons/{uuid}')

    assert response.status == 200
    assert response.body['full_name'] == 'abc'
