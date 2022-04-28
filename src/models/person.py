from typing import Optional
from uuid import UUID

from pydantic import Field

from .base_models import BaseApiConfig
from .base_models import BaseApiModel


class PersonShort(BaseApiModel):
    full_name: str = Field(alias='name')


class Person(BaseApiConfig):
    name: str
    roles: list[str] | None
    films_as_actor: Optional[list[str]]
    films_as_director: Optional[list[str]]
    films_as_writer: Optional[list[str]]


class ResponsePerson(PersonShort):
    roles: list[str] | None
    actor_ids: list[UUID] | None = Field(alias='films_as_actor')
    writer_ids: list[UUID] | None = Field(alias='films_as_writer')
    director_ids: list[UUID] | None = Field(alias='films_as_director')
