from uuid import UUID

from pydantic import BaseModel, Field


class BaseApiModel(BaseModel):
    uuid: UUID = Field(alias='id')


class Genre(BaseApiModel):
    name: str


class PersonShort(BaseApiModel):
    full_name: str = Field(alias='name')


class Person(PersonShort):
    roles: list[str] | None
    actor_ids: list[UUID] | None = Field(alias='films_as_actor')
    writer_ids: list[UUID] | None = Field(alias='films_as_writer')
    director_ids: list[UUID] | None = Field(alias='films_as_director')


class FilmList(BaseApiModel):
    title: str
    imdb_rating: float | None


class FilmDetail(FilmList):
    description: str | None
    genre: list[Genre] | None
    actors: list[PersonShort] | None
    writers: list[PersonShort] | None
    directors: list[PersonShort] | None = Field(alias='director')
