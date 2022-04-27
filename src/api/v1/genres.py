import logging

from fastapi import APIRouter, Depends, Request

from services.genres import GenreService, get_genre_service

from .base import item_details, item_list
from .models import Genre

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/{genre_id}', response_model=Genre, response_model_by_alias=False)
async def genre_item(genre_id: str, item_service: GenreService = Depends(get_genre_service)):
    return await item_details(genre_id, item_service)


@router.get('/', response_model=list[Genre], response_model_by_alias=False)
async def genre_list(request: Request, item_service: GenreService = Depends(get_genre_service)) -> list:
    return await item_list(item_service, request)
