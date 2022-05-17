import pytest
from aioredis import Redis
from elasticsearch import AsyncElasticsearch

from ..testdata.movies import Movies

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize('query, page_number, page_size, expected_status, expected_body, cache_size', [
    ('Wars', 1, 10, 200, [Movies.expected_short()[1]], 1),
    ('Harrison', 1, -1, 422, Movies.errors['not_gt_size'], 0),
    ('trek', 1, 10, 200, [Movies.expected_short()[0]], 1),
    ('Star', 1, 10, 200, Movies.expected_short(), 1),
    ('Star', 2, 1, 200, [Movies.expected_short()[1]], 1),
    ('1337', 1, 1, 200, [], 0),
    ('13', 0, 1, 422, Movies.errors['not_gt_number'], 0),
    ('14', 1, 'q', 422, Movies.errors['int_size'], 0),
    (1337, 1, 1, 200, [], 0)
])
async def test_movies_search(
        fill_db_movies, redis_client: Redis, get_request, query: str | int, page_number: int | str,
        page_size: int | str, expected_status: int, expected_body: dict | list, cache_size: int
):
    response = await get_request(f'/films/search?query={query}&page[number]={page_number}&page[size]={page_size}')

    assert response.status == expected_status
    assert response.body == expected_body
    assert await redis_client.dbsize() == cache_size


@pytest.mark.parametrize('reverse', [True, False])
async def test_search_sort(fill_db_movies, get_request, reverse: bool):
    response = await get_request(
        f'/films/search?query=Star&sort={"-" if reverse else ""}imdb_rating&page[number]=1&page[size]=10')
    expected = Movies.expected_short()
    expected.sort(reverse=reverse, key=lambda i: i['imdb_rating'])

    assert response.status == 200
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.parametrize('reverse', [True, False])
async def test_film_sort(fill_db_movies, get_request, reverse: bool):
    response = await get_request(f'/films?sort={"-" if reverse else ""}imdb_rating')
    expected = Movies.expected_short()
    expected.sort(reverse=reverse, key=lambda i: i['imdb_rating'])

    assert response.status == 200
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.parametrize('reverse', [True, False])
@pytest.mark.parametrize('page_number', [1, 2])
async def test_film_sort_pagination(fill_db_movies, get_request, page_number: int, reverse: bool):
    page_size = 1
    response = await get_request(f'/films?sort={"-" if reverse else ""}imdb_rating&'
                                 f'page[number]={page_number}&page[size]={page_size}')
    expected = Movies.expected_short()
    expected.sort(reverse=reverse, key=lambda i: i['imdb_rating'])
    portion = page_size * (page_number - 1)
    expected = expected[portion: portion + page_size]

    assert response.status == 200
    assert len(response.body) == page_size
    assert response.body == expected


@pytest.mark.parametrize('genre, count', Movies.genres)
async def test_film_filter(fill_db_movies, get_request, genre: list, count: list):
    response = await get_request(f'/films?filter[genre]={genre}')

    assert response.status == 200
    assert len(response.body) == count


@pytest.mark.parametrize('uuid', [Movies.data[0]['id']])
async def test_film_id(fill_db_movies, get_request, uuid: str):
    response = await get_request(f'/films/{uuid}')

    expected = Movies.expected()
    assert response.status == 200
    assert len(response.body) == 8
    assert response.body == expected[0]


@pytest.mark.parametrize('page_number, size', [(0, 1), (1, 0), (-1, 1), (1, -1), ('asdfg', 1), (1, 'asdf')])
async def test_wrong_parameters(fill_db_movies, get_request, page_number: str | int, size: str | int):
    response = await get_request(f'/films?page[number]={page_number}&page[size]={size}')

    assert response.status == 422


async def test_wrong_film_id(fill_db_movies, get_request):
    response = await get_request('/films/121212312313134')

    assert response.status == 404
