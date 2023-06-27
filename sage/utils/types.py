from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Sequence, Tuple
from uuid import uuid4

from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, PositiveInt


class RoundTypes(str, Enum):
    match_play = "match"
    stroke_play = "stroke"


class BaseModel(PydanticBaseModel):
    class Config:
        underscore_attrs_are_private = True
        use_enum_values = True


class Hole(BaseModel):
    number: Optional[PositiveInt] = None
    par: Optional[PositiveInt] = None
    yardage: Optional[PositiveInt] = None
    score: Optional[PositiveInt] = None
    putts: Optional[PositiveInt] = None
    handicap: Optional[PositiveInt] = None

    _adjusted_score: Optional[PositiveInt] = None
    _net_par: Optional[PositiveInt] = None

    def reset(self) -> None:
        self._adjusted_score = None
        self._net_par = None

    def net_par(self, handicap_index: int = 0) -> PositiveInt:
        """
        The estimated score of a player based on their handicap index if they don't play a hole.
        """
        if self._net_par is None:
            self._net_par = self.par if handicap_index > self.handicap else self.par + 1
        return self._net_par

    def adjusted_score(self, handicap_index: int = 0) -> PositiveInt:
        """
        Adapted from the USGA score adjustment page
        https://www.usga.org/content/usga/home-page/handicapping/world-handicap-system/world-handicap-system-usga-golf-faqs/faqs---what-is-the-maximum-hole-score-.html
        """
        if self._adjusted_score is None:
            # Make handicap index -1 for initial round
            if handicap_index < 0:
                max_score = self.par + 5
            # Once we have a handicap, pass that through
            elif (
                handicap_index > 0 and handicap_index <= self.handicap
            ) or handicap_index > 18:
                max_score = self.par + 3
            # Scratch golfers don't get extra strokes
            else:
                max_score = self.par + 2
            if self.score is None:
                self.score = self.net_par(handicap_index)
            self._adjusted_score = self.score if self.score < max_score else max_score
        return self._adjusted_score


class Round(BaseModel):
    id: str = Field(default_factory=uuid4)
    tees: str
    date: datetime
    course: str
    slope: PositiveInt
    rating: float
    holes: Sequence[Hole] = []
    user: Optional[str] = None
    score: Optional[PositiveInt] = None
    pcc: int = 0
    exceptional_round: bool = False
    exceptional_adjustment_strokes: PositiveInt = 0
    competition: bool = False
    round_type: RoundTypes = RoundTypes.stroke_play

    _valid_round: bool = False
    _adjusted_gross_score: Optional[int] = None
    _score_differential: Optional[float] = None

    def reset(self) -> None:
        self._valid_round = False
        self._adjusted_gross_score = None
        self._score_differential = None

    def __lt__(self, other: Round) -> bool:
        assert self._adjusted_gross_score is not None, "Can't compare NoneType to int"
        return self._adjusted_gross_score < other._adjusted_gross_score

    def __gt__(self, other: Round) -> bool:
        assert self._adjusted_gross_score is not None, "Can't compare NoneType to int"
        return self._adjusted_gross_score > other._adjusted_gross_score

    def __eq__(self, other: Round) -> bool:
        return self._adjusted_gross_score == other._adjusted_gross_score

    @property
    def is_valid(self) -> bool:
        self._valid_round = len(self.holes) == 18
        return self._valid_round

    def exceptional_adjustment(self, strokes: PositiveInt):
        """
        The number of strokes to take away from the adjusted gross score due to
        posting an exceptional round
        """
        self.exceptional_adjustment_strokes += strokes

    def adjusted_gross_score(self, handicap_index: int = 0) -> int:
        """
        The adjusted score used to level out poor performance on individual holes.
        """
        self._adjusted_gross_score = 0
        for hole in self.holes:
            self._adjusted_gross_score += hole.adjusted_score(handicap_index)
        self._adjusted_gross_score -= self.exceptional_adjustment_strokes

        return self._adjusted_gross_score

    def score_differential(self, handicap_index: int = 0) -> Tuple[float, bool]:
        """
        Adapted from USGA score differential page
        https://www.usga.org/content/usga/home-page/handicapping/world-handicap-system/world-handicap-system-usga-golf-faqs/faqs---what-is-a-score-differential.html
        """
        self._score_differential = (113 / self.slope) * (
            self.adjusted_gross_score(handicap_index) - self.rating - self.pcc
        )
        if handicap_index - self._score_differential >= 7:
            self.exceptional_round = True
        else:
            self.exceptional_round = False
        return self._score_differential, self.exceptional_round


Rounds = Dict[str, Round]


class CourseHandicapRequest(BaseModel):
    rating: int
    slope: float
    par: int


class PlayingHandicapRequest(CourseHandicapRequest):
    allowance: int
