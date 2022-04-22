from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from models.base_models import BaseApiConfig
from .genre import Genre
from .person import Person


class Film(BaseApiConfig):
    title: str
    description: Optional[str]
    imdb_rating: float
    creation_date: datetime | None
    genre: list[Genre]
    actors: list[Person]
    writers: list[Person]
    directors: list[Person]
    actors_names: Optional[list[str]] | Optional[str]
    writers_names: Optional[list[str]] | Optional[str]
    directors_names: Optional[list[str]] | Optional[str]
