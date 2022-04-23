from models.base_models import BaseApiConfig


class Person(BaseApiConfig):
    name: str
    role: list[str] | None
    film_ids: list[str] | None
