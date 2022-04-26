from typing import Optional

from models.base_models import BaseApiConfig


class Person(BaseApiConfig):
    full_name: str
    roles: list[str] | None
    films_as_actor: Optional[list[str]] | Optional[str]
    films_as_director: Optional[list[str]] | Optional[str]
    films_as_writer: Optional[list[str]] | Optional[str]
