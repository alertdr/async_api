from datetime import datetime
from typing import Optional

from pydantic import Field

from .base_models import BaseApiConfig, BaseApiModel
from .genre import Genre
from .person import Person, PersonShort


class Film(BaseApiConfig):
    title: str
    description: Optional[str]
    imdb_rating: float | None
    creation_date: datetime | None
    genre: list[Genre] | None
    actors: list[Person] | None
    writers: list[Person] | None
    director: list[Person] | None
    actors_names: Optional[list[str]] | Optional[str]
    writers_names: Optional[list[str]] | Optional[str]
    directors_names: Optional[list[str]] | Optional[str]


class FilmList(BaseApiModel):
    title: str
    imdb_rating: float | None


class FilmDetail(FilmList):
    description: str | None
    genre: list[Genre] | None
    actors: list[PersonShort] | None
    writers: list[PersonShort] | None
    directors: list[PersonShort] | None = Field(alias='director')
