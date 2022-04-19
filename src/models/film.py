from dataclasses import dataclass
from typing import Optional

from models.base_models import BaseApiConfig


@dataclass
class Film(BaseApiConfig):
    title: str
    description: Optional[str]
    imdb_rating: float
    genre: Optional[list[str]]
    actors: Optional[list[dict]]
    writers: Optional[list[dict]]
    director: Optional[list[str]]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
