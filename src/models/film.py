from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.base_models import BaseApiConfig


@dataclass
class Film(BaseApiConfig):
    title: str
    description: Optional[str]
    imdb_rating: float
    creation_date: datetime
    genre: Optional[list[str]]
    actors: Optional[list[dict]]
    writers: Optional[list[dict]]
    directors: Optional[list[dict]]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    directors_names: Optional[list[str]]
