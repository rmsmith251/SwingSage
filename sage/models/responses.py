from __future__ import annotations

from sage.models.base import BaseModel
from sage.models.golf import Hole, KeyRoundData


class ScoreResponse(BaseModel):
    strokes: int = 0
    current_par: int = 0
    score: int = 0
    holes_completed: int = 0

    def update(self, hole: Hole):
        if hole.score is not None:
            self.strokes += hole.score
            self.current_par += hole.par
            self.score += hole.strokes - hole.par
            self.holes_completed += 1


class RoundsResponse(BaseModel):
    rounds: list[KeyRoundData]
