import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import Field

from services.persons import PersonService, get_person_service

from .base import BaseApiModel, BaseDataModel, item_details, item_list

logger = logging.getLogger(__name__)
router = APIRouter()


class PersonShort(BaseApiModel):
    full_name: str = Field(alias='name')


class Person(PersonShort):
    role: str
    film_ids: list[UUID]


@router.get('/{person_id}/film/')
async def redirect_to_films(person_id: str, item_service: PersonService = Depends(get_person_service)):
    person = await person_item(person_id, item_service)
    path = f'/api/v1/films?filter={person.film_ids}'
    logger.debug('Redirect to %s', path)
    return RedirectResponse(path)


@router.get('/{person_id}', response_model=Person, response_model_by_alias=False)
async def person_item(person_id: str, item_service: PersonService = Depends(get_person_service)) -> BaseDataModel:
    return await item_details(person_id, item_service)


@router.get('/', response_model=list[Person], response_model_by_alias=False)
async def person_list(request: Request,
                      item_service: PersonService = Depends(get_person_service)) -> list[BaseDataModel]:
    return await item_list(item_service, request)
