
from asyncio.log import logger
from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException, Request
from pydantic import BaseModel, Field

from models.base_models import BaseApiConfig as BaseDataModel
from services.basic import BaseService

from .tools import parse_brackets_params


class BaseApiModel(BaseModel):
    uuid: UUID = Field(alias='id')


async def item_details(item_id: str, item_service: BaseService) -> BaseDataModel:
    item = await item_service.get_by_id(item_id)
    logger.debug('api model %s', item)
    if not item:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='nothing found')
    return item


async def item_list(item_service: BaseService, request: Request, **kwargs) -> list[BaseDataModel]:
    params = parse_brackets_params(request.query_params)
    params.update(kwargs)
    items = await item_service.get_list(**params)
    return items
