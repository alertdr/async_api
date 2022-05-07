import logging

from fastapi import APIRouter, Depends, Query

from models.genre import ResponseGenre
from services.genres import GenreService, get_genre_service

from .base import item_details, item_list, pagination

logger = logging.getLogger(__name__)
router = APIRouter()


def sorting(sort: str = Query(None, description='Sort query by fields: "name" (-field for desc)')) -> str | None:
    if sort and sort.lstrip('-') in ('name',):
        return sort


@router.get('/{genre_id}', response_model=ResponseGenre, response_model_by_alias=False)
async def genre_item(genre_id: str, item_service: GenreService = Depends(get_genre_service)):
    return await item_details(genre_id, item_service)


@router.get('/', response_model=list[ResponseGenre], response_model_by_alias=False)
async def genre_list(
        page=Depends(pagination),
        sort=Depends(sorting),
        item_service: GenreService = Depends(get_genre_service),
) -> list:
    return await item_list(item_service, page=page, sort=sort)
