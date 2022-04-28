import logging

from fastapi import APIRouter, Depends, Query

from models.response_models import FilmDetail, FilmList
from services.films import FilmService, get_film_service

from .base import item_details, item_list, pagination, searching

logger = logging.getLogger(__name__)
router = APIRouter()


def filtering(
        genre: str = Query(None, alias='filter[genre]', description='Filter by genre'),
        person: str = Query(None, alias='filter[person]', description='Filter by actor, writer, director'),
) -> dict[str, str | None]:
    filter: dict[str, str | None] = {'genre': genre, 'person': person}
    return filter


def sorting(sort: str = Query(None, description='Sort query by field (-field for desc)')) -> str | None:
    if sort and sort.lstrip('-') in ('imdb_rating'):
        return sort


@router.get('/search', response_model=list[FilmList], response_model_by_alias=False)
async def film_search_list(
        query=Depends(searching),
        page=Depends(pagination),
        sort=Depends(sorting),
        list_service: FilmService = Depends(get_film_service)
) -> list:
    return await item_list(list_service, query=query, page=page, sort=sort)


@router.get('/{film_id}', response_model=FilmDetail, response_model_by_alias=False)
async def film_item(film_id: str, item_service: FilmService = Depends(get_film_service)):
    return await item_details(film_id, item_service)


@router.get('/', response_model=list[FilmList], response_model_by_alias=False)
async def film_list(
        filter=Depends(filtering),
        page=Depends(pagination),
        sort=Depends(sorting),
        list_service: FilmService = Depends(get_film_service),
) -> list:
    return await item_list(list_service, filter=filter, page=page, sort=sort)
