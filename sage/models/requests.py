from __future__ import annotations

from datetime import datetime

from pydantic import PositiveInt

from sage.models.base import BaseModel


class CourseHandicapRequest(BaseModel):
    rating: int
    slope: float
    par: int


class PlayingHandicapRequest(CourseHandicapRequest):
    allowance: int


class StartRoundRequest(BaseModel):
    tees: str
    date: datetime
    course: str
    slope: PositiveInt
    rating: float
