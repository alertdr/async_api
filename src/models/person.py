from dataclasses import dataclass
from typing import Optional

from models.base_models import BaseApiConfig


@dataclass
class Person(BaseApiConfig):
    full_name: str
    role: list[str]
    film_ids: dict[dict[str, Optional[list[str]]]]


