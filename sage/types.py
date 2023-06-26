from datetime import datetime
from typing import Optional, Sequence

from pydantic import BaseModel as PydanticBaseModel
from pydantic import PositiveInt


class BaseModel(PydanticBaseModel):
    class Config:
        underscore_attrs_are_private = True


class Hole(BaseModel):
    number: Optional[PositiveInt] = None
    par: Optional[PositiveInt] = None
    yardage: Optional[PositiveInt] = None
    score: Optional[PositiveInt] = None
    putts: Optional[PositiveInt] = None
    handicap: Optional[PositiveInt] = None


class Round(BaseModel):
    tees: str
    date: datetime
    course: str
    slope: PositiveInt
    rating: float
    holes: Sequence[Hole] = []


Rounds = Sequence[Round]
