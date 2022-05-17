import logging

from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse

from models.person import ResponsePerson
from services.persons import PersonService, get_person_service

from .base import item_details, item_list, pagination, searching

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('/{person_id}/film/')
async def redirect_to_films(person_id: str):
    path = f'/api/v1/films?filter[person]={person_id}'
    logger.debug('Redirect to %s', path)
    return RedirectResponse(path)


@router.get('/search',
            response_model=list[ResponsePerson],
            response_model_by_alias=False,
            response_model_exclude_none=True)
async def person_search_list(query=Depends(searching),
                             page=Depends(pagination),
                             list_service: PersonService = Depends(get_person_service)) -> list:
    return await item_list(list_service, query=query, page=page)


@router.get('/{person_id}',
            response_model=ResponsePerson,
            response_model_by_alias=False,
            response_model_exclude_none=True)
async def person_item(person_id: str, item_service: PersonService = Depends(get_person_service)):
    return await item_details(person_id, item_service)


@router.get('/', response_model=list[ResponsePerson], response_model_by_alias=False, response_model_exclude_none=True)
async def person_list(page=Depends(pagination),
                      list_service: PersonService = Depends(get_person_service)) -> list:
    return await item_list(list_service, page=page)
