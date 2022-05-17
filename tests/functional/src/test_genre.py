import pytest
from elasticsearch import AsyncElasticsearch
from redis import Redis

from ..testdata.genres import Genres

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize('reverse', [True, False])
@pytest.mark.parametrize('page_number', [1, 2])
async def test_genres_sort_pagination(fill_db_genres, get_request, reverse: bool, page_number: int):
    page_size = 1
    response = await get_request(f'/genres?sort={"-" if reverse else ""}name&'
                                 f'page[number]={page_number}&page[size]={page_size}')
    expected = Genres.expected.copy()
    expected.sort(reverse=reverse, key=lambda i: i['name'])
    portion = page_size * (page_number - 1)
    expected = expected[portion: portion + page_size]

    assert response.status == 200
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.parametrize('uuid', [item['id'] for item in Genres.data])
async def test_film_id(fill_db_genres, get_request, uuid):
    response = await get_request(f'/genres/{uuid}')
    expected = Genres.expected.copy()

    assert response.status == 200
    assert len(response.body) == 2
    assert response.body in expected


@pytest.mark.parametrize('page_number, size', [(0, 1), (1, 0), (-1, 1), (1, -1), ('asdfg', 1), (1, 'asdf')])
async def test_wrong_parameters(fill_db_genres, get_request, page_number, size):
    response = await get_request(f'/genres?page[number]={page_number}&page[size]={size}')

    assert response.status == 422


async def test_wrong_genre_id(fill_db_genres, get_request):
    response = await get_request('/genres/121212312313134')

    assert response.status == 404


@pytest.mark.parametrize('uuid', [Genres.data[0]['id']])
async def test_redis(fill_db_genres, redis_client: Redis, es_client: AsyncElasticsearch, get_request, uuid):
    expected = Genres.expected[0]

    assert await redis_client.dbsize() == 0

    response = await get_request(f'/genres/{uuid}')

    assert response.status == 200
    assert await redis_client.dbsize() == 1

    await es_client.update('genres', uuid, body={'doc': {'name': 'Some words...'}}, refresh=True)
    response = await get_request(f'/genres/{uuid}')

    assert response.status == 200
    assert response.body == expected

    await redis_client.flushdb(asynchronous=True)

    response = await get_request(f'/genres/{uuid}')
    assert response.status == 200
    assert response.body['name'] == 'Some words...'
