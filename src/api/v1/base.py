
import logging
from http import HTTPStatus

from fastapi import HTTPException, Request

from models.base_models import BaseApiConfig as BaseDataModel
from services.basic import BaseService

from .tools import parse_brackets_params

logger = logging.getLogger(__name__)


async def item_details(item_id: str, item_service: BaseService) -> BaseDataModel:
    item = await item_service.get_by_id(item_id)
    logger.debug('api model %s', item)
    if not item:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='nothing found')
    return item


async def item_list(list_service: BaseService, request: Request, **kwargs) -> list[BaseDataModel]:
    params = parse_brackets_params(request.query_params)
    params.update(kwargs)
    items = await list_service.get_list(**params)
    return items
