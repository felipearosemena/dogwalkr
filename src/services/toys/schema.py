from datetime import datetime
from typing import List

from pydantic import BaseModel

from ..common.schema import Meta


class Toy(BaseModel):
    id: int
    name: str
    dog_owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ToysResponse(BaseModel):
    meta: Meta
    toys: List[Toy]
