import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

import api.v1.persons as persons
from services.films import FilmService, get_film_service

from .base import item_details, item_list
from .genres import Genre

logger = logging.getLogger(__name__)
router = APIRouter()


class FilmList(BaseModel):
    uuid: UUID = Field(alias='id')
    title: str
    imdb_rating: float | None


class FilmDetail(FilmList):
    description: str | None
    genre: list[Genre] | None
    actors: list[persons.PersonShort] | None
    writers: list[persons.PersonShort] | None
    directors: list[persons.PersonShort] | None


@router.get('/{film_id}', response_model=FilmDetail, response_model_by_alias=False)
async def film_item(film_id: str, item_service: FilmService = Depends(get_film_service)):
    return await item_details(film_id, item_service)


@router.get('/', response_model=list[FilmList], response_model_by_alias=False)
async def film_list(request: Request, item_service: FilmService = Depends(get_film_service)) -> list:
    return await item_list(item_service, request)
