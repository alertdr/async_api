from typing import Optional

from models.base_models import BaseApiConfig


class Genre(BaseApiConfig):
    name: str
    description: Optional[str]
