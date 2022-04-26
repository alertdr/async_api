from datetime import datetime
from typing import Optional

from models.base_models import BaseApiConfig

from .genre import Genre
from .person import Person


class Film(BaseApiConfig):
    title: str
    description: Optional[str]
    imdb_rating: float | None
    creation_date: datetime | None
    genre: list[Genre] | None
    actors: list[Person] | None
    writers: list[Person] | None
    directors: list[Person] | None
    actors_names: Optional[list[str]] | Optional[str]
    writers_names: Optional[list[str]] | Optional[str]
    directors_names: Optional[list[str]] | Optional[str]
