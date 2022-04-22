
from asyncio.log import logger
from http import HTTPStatus
from uuid import UUID

import orjson
from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel, Field
from services.basic import BaseService

from .tools import parse_brackets_params


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseApiModel(BaseModel):
    uuid: UUID = Field(alias='id')

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


async def item_details(item_id: str, item_service: BaseService, model):
    item = await item_service.get_by_id(item_id)
    logger.debug('api model %s', item)
    if not item:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='nothing found')
    return model.schema
    return model(**item.dict())


async def item_list(item_service: BaseService, model, request: Request, **kwargs) -> list:
    params = parse_brackets_params(request.query_params)
    params.update(kwargs)
    items = await item_service.get_list(**params)
    return [model(**item.dict()) for item in items]
