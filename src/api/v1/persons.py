from pydantic import BaseModel
from uuid import UUID


class PersonShort(BaseModel):
    uuid: UUID
    full_name: str


class Person(PersonShort):
    role: str
    film_ids: list[UUID]
