from typing import Optional

from .base_models import BaseApiConfig
from .base_models import BaseApiModel


class Genre(BaseApiConfig):
    name: str
    description: Optional[str]


class ResponseGenre(BaseApiModel):
    name: str
