import pytest

from testdata.movies_data import Movies


@pytest.mark.asyncio
@pytest.mark.parametrize('reverse', [True, False])
async def ttest_get_film_list_with_sort(fill_db, make_get_request, reverse: bool):
    response = await make_get_request(f'/films?sort={"-" if reverse else ""}imdb_rating')
    expected = Movies.expected_short()
    expected.sort(reverse=reverse, key=lambda i: i['imdb_rating'])
    assert response.status == 200
    assert len(response.body) == len(expected)
    assert response.body == expected


@pytest.mark.asyncio
@pytest.mark.parametrize('reverse', [True, False])
@pytest.mark.parametrize('page_number', [1, 2])
async def ttest_get_film_list_with_sort_and_pagination(fill_db, make_get_request, page_number: int, reverse: bool):
    page_size = 1
    response = await make_get_request(f'/films?sort={"-" if reverse else ""}imdb_rating&'
                                      f'page[number]={page_number}&page[size]={page_size}')
    expected = Movies.expected_short()
    expected.sort(reverse=reverse, key=lambda i: i['imdb_rating'])
    slice = page_size * (page_number - 1)
    expected = expected[slice: slice + page_size]
    assert response.status == 200
    assert len(response.body) == page_size
    assert response.body == expected


@pytest.mark.asyncio
@pytest.mark.parametrize('genre, count', Movies.genres)
async def test_get_film_list_filtered(fill_db, make_get_request, genre, count):
    response = await make_get_request(f'/films?filter[genre]={genre}')
    assert response.status == 200
    assert len(response.body) == count