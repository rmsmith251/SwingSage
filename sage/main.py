from typing import Union

from sage.models.golf import Round, Rounds
from sage.models.requests import CourseHandicapRequest, PlayingHandicapRequest


def course_handicap(
    handicap_index: float, request: Union[CourseHandicapRequest, PlayingHandicapRequest]
) -> float:
    return handicap_index * (request.slope / 113) + (request.rating - request.par)


def playing_handicap(user_id: str, request: PlayingHandicapRequest) -> int:
    return round(course_handicap(user_id, request) * request.allowance)


def exceptional_adjustment(diff: float):
    pass


def calculate_handicap_index(rounds: Rounds, current_handicap_index: float) -> float:
    assert (
        len(rounds) >= 3
    ), "At least 3 rounds are required to calculate a handicap index"
    current_handicap_index = -1
    score_diffs = [
        rnd.score_differential(current_handicap_index)[0] for rnd in rounds.values()
    ]
    return round(sum(score_diffs) / len(score_diffs), 2)


def add_new_round(user_id: str, round: Round):
    diff = 2
    exceptional_adjustment(diff)
    pass
