import logging

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from services.persons import PersonService, get_person_service

from .base import item_details, item_list
from .models import Person

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/{person_id}/film/')
async def redirect_to_films(person_id: str):
    path = f'/api/v1/films?filter[person]={person_id}'
    logger.debug('Redirect to %s', path)
    return RedirectResponse(path)


@router.get('/search', response_model=list[Person], response_model_by_alias=False, response_model_exclude_none=True)
async def person_search_list(query,
                             request: Request,
                             list_service: PersonService = Depends(get_person_service)) -> list:
    return await item_list(list_service, request)


@router.get('/{person_id}', response_model=Person, response_model_by_alias=False, response_model_exclude_none=True)
async def person_item(person_id: str, item_service: PersonService = Depends(get_person_service)):
    return await item_details(person_id, item_service)


@router.get('/', response_model=list[Person], response_model_by_alias=False, response_model_exclude_none=True)
async def person_list(request: Request,
                      list_service: PersonService = Depends(get_person_service)) -> list:
    return await item_list(list_service, request)
