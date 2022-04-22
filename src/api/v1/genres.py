import logging

from fastapi import APIRouter, Depends, Request
from services.genres import GenreService, get_genre_service

from .base import BaseApiModel, item_details, item_list

logger = logging.getLogger(__name__)
router = APIRouter()


class Genre(BaseApiModel):
    name: str


@router.get('/{genre_id}')
async def film_item(genre_id: str, item_service: GenreService = Depends(get_genre_service)) -> Genre:
    return await item_details(genre_id, item_service, Genre)


@router.get('/')
async def film_list(request: Request, item_service: GenreService = Depends(get_genre_service)) -> list[Genre]:
    return await item_list(item_service, Genre, request)
