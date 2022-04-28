import logging

from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse

from models.response_models import Person
from services.persons import PersonService, get_person_service

from .base import item_details, item_list, pagination, searching

logger = logging.getLogger(__name__)
router = APIRouter()


def sorting(sort: str = Query(None, description='Sort query by field (-field for desc)')) -> str | None:
    if sort and sort.lstrip('-') in ('full_name'):
        return sort


@router.get('/{person_id}/film/')
async def redirect_to_films(person_id: str):
    path = f'/api/v1/films?filter[person]={person_id}'
    logger.debug('Redirect to %s', path)
    return RedirectResponse(path)


@router.get('/search', response_model=list[Person], response_model_by_alias=False, response_model_exclude_none=True)
async def person_search_list(query=Depends(searching),
                             page=Depends(pagination),
                             sort=Depends(sorting),
                             list_service: PersonService = Depends(get_person_service)) -> list:
    return await item_list(list_service, query=query, page=page, sort=sort)


@router.get('/{person_id}', response_model=Person, response_model_by_alias=False, response_model_exclude_none=True)
async def person_item(person_id: str, item_service: PersonService = Depends(get_person_service)):
    return await item_details(person_id, item_service)


@router.get('/', response_model=list[Person], response_model_by_alias=False, response_model_exclude_none=True)
async def person_list(page=Depends(pagination),
                      sort=Depends(sorting),
                      list_service: PersonService = Depends(get_person_service)) -> list:
    return await item_list(list_service, page=page, sort=sort)
