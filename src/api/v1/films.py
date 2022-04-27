import logging

from fastapi import APIRouter, Depends, Request

from services.films import FilmService, get_film_service

from .base import item_details, item_list
from .models import FilmDetail, FilmList

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/search', response_model=list[FilmList], response_model_by_alias=False)
async def film_search_list(query, request: Request, list_service: FilmService = Depends(get_film_service)) -> list:
    return await item_list(list_service, request, query=query)


@router.get('/{film_id}', response_model=FilmDetail, response_model_by_alias=False)
async def film_item(film_id: str, item_service: FilmService = Depends(get_film_service)):
    return await item_details(film_id, item_service)


@router.get('/', response_model=list[FilmList], response_model_by_alias=False)
async def film_list(request: Request, list_service: FilmService = Depends(get_film_service)) -> list:
    return await item_list(list_service, request)
