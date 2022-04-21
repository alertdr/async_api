from typing import Optional

from models.base_models import BaseApiConfig


class Film(BaseApiConfig):
    id: str
    title: str
    description: Optional[str]
    imdb_rating: float
    genre: Optional[list[dict[str, str]]]
    actors: Optional[list[dict[str, str]]]
    writers: Optional[list[dict[str, str]]]
    director: Optional[str]
    actors_names: Optional[str]
    writers_names: Optional[str]
