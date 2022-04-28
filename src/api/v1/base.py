
import logging
from http import HTTPStatus

from fastapi import HTTPException, Query

from models.base_models import BaseApiConfig as BaseDataModel
from services.basic import BaseService

logger = logging.getLogger(__name__)

DEFAULT_PAGE_PARAMS: dict[str, int] = {
    'size': 10,
    'number': 1,
}


def pagination(
        page_size: int = Query(
            DEFAULT_PAGE_PARAMS['size'],
            gt=0,
            alias='page[size]',
            description='Items amount on page',
        ),
        page_number: int = Query(
            DEFAULT_PAGE_PARAMS['number'],
            gt=0,
            alias='page[number]',
            description='Page number for pagination',
        ),
) -> dict[str, int]:
    return {'size': page_size, 'number': page_number}


def searching(query: str = Query(..., description='Search query')) -> str:
    return query


async def item_details(item_id: str, item_service: BaseService) -> BaseDataModel:
    item = await item_service.get_by_id(item_id)
    logger.debug('api model %s', item)
    if not item:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='nothing found')
    return item


async def item_list(list_service: BaseService, **kwargs) -> list[BaseDataModel]:
    items = await list_service.get_list(**kwargs)
    return items
