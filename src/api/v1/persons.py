import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field
from services.persons import PersonService, get_person_service
from services.films import FilmService
from models.film import Film

from .base import item_details, item_list

logger = logging.getLogger(__name__)
router = APIRouter()


class PersonShort(BaseModel):
    uuid: UUID = Field(alias='id')
    full_name: str


class Person(PersonShort):
    role: str
    film_ids: list[UUID]


@router.get('/{person_id}/film/')
async def films_by_person(person_id, request: Request,
                          item_service: FilmService = Depends(get_person_service)) -> list[Film]:
    filter = {'actor': person_id}
    return await item_list(item_service, FilmService, request, filter=filter)


@router.get('/{person_id}')
async def person_item(person_id: str, item_service: PersonService = Depends(get_person_service)) -> Person:
    return await item_details(person_id, item_service, Person)


@router.get('/')
async def person_list(request: Request, item_service: PersonService = Depends(get_person_service)) -> list[PersonShort]:
    return await item_list(item_service, PersonShort, request)
