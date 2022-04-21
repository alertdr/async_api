import re
import logging
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from services.films import (FilmDetailService, FilmListService,
                            get_film_list_service, get_film_service)

from .genres import Genre
from .persons import PersonShort

logger = logging.getLogger(__name__)
router = APIRouter()


class FilmList(BaseModel):
    uuid: UUID = Field(alias='id')
    title: str
    imdb_rating: float | None


class FilmDetail(FilmList):
    description: str | None
    genre: list[Genre] | None
    actors: list[PersonShort] | None
    writers: list[PersonShort] | None
    directors: list[PersonShort] | None


@router.get('/{film_id}')
async def film_details(film_id: str, film_service: FilmDetailService = Depends(get_film_service)) -> FilmDetail:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return FilmDetail(**film.dict())


def parse_brackets_params(param) -> dict:
    params = {}
    regex = r'(?P<op>.*)\[(?P<col>.*)\]'
    for key, value in dict(param).items():
        if m := re.search(regex, key):
            if m.group("op") in params:
                params[m.group("op")].update({m.group("col"): value})
            else:
                params.update({m.group("op"): {m.group("col"): value}})
        else:
            params.update({key: value})
    return params


@router.get('/')
async def film_list(request: Request,
                    film_list_service: FilmListService = Depends(get_film_list_service)) -> list[FilmList]:
    params = parse_brackets_params(request.query_params)
    film_list = await film_list_service.get_film_list(**params)
    return [FilmList(**film.dict()) for film in film_list]
