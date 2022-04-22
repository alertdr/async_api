from pydantic import Field
from models.base_models import BaseApiConfig


class Person(BaseApiConfig):
    full_name: str = Field(alias='name')
    role: list[str] | None
    film_ids: list[str] | None
