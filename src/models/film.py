from typing import Optional

from models.base_models import BaseApiConfig


class Film(BaseApiConfig):
    id: str
    title: str
    description: Optional[str]
    imdb_rating: float
    genre: Optional[list[Optional[str]]]
    actors: Optional[list[Optional[dict]]]
    writers: Optional[list[Optional[dict]]]
    director: Optional[list[Optional[str]]]
    actors_names: Optional[list[Optional[str]]]
    writers_names: Optional[list[Optional[str]]]
