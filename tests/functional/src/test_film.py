import pytest

from ..testdata.movies import Movies

pytestmark = pytest.mark.asyncio


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
async def test_film_filter(fill_db_movies, get_request, genre, count):
    response = await get_request(f'/films?filter[genre]={genre}')

    assert response.status == 200
    assert len(response.body) == count


@pytest.mark.parametrize('uuid', [Movies.data[0]['id']])
async def test_film_id(fill_db_movies, get_request, uuid):
    response = await get_request(f'/films/{uuid}')

    expected = Movies.expected()
    assert response.status == 200
    assert len(response.body) == 8
    assert response.body == expected[0]


@pytest.mark.parametrize('page_number, size', [(0, 1), (1, 0), (-1, 1), (1, -1), ('asdfg', 1), (1, 'asdf')])
async def test_wrong_parameters(fill_db_movies, get_request, page_number, size):
    response = await get_request(f'/films?page[number]={page_number}&page[size]={size}')

    assert response.status == 422


async def test_wrong_film_id(fill_db_movies, get_request):
    response = await get_request('/films/121212312313134')

    assert response.status == 404
