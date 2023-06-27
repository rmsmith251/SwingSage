import json
from typing import Union

from pydantic import parse_obj_as

from sage.utils.types import (
    CourseHandicapRequest,
    PlayingHandicapRequest,
    Round,
    Rounds,
)


def course_handicap(
    user_id: str, request: Union[CourseHandicapRequest, PlayingHandicapRequest]
) -> float:
    # handicap_index = get_user_handicap(user_id)
    handicap_index = 2
    return handicap_index * (request.slope / 113) + (request.rating - request.par)


def playing_handicap(user_id: str, request: PlayingHandicapRequest) -> int:
    return round(course_handicap(user_id, request) * request.allowance)


def exceptional_adjustment(diff: float):
    pass


def calculate_handicap_index(user_id: str) -> float:
    # rounds = sorted(get_last_twenty_rounds(user_id))
    # current_handicap_index = get_user_handicap(user_id)
    with open("tests/assets/example_round.json", "r") as f:
        data = json.load(f)

    rounds = parse_obj_as(Rounds, data)

    assert (
        len(rounds) >= 3
    ), "At least 3 rounds are required to calculate a handicap index"
    current_handicap_index = -1
    score_diffs = [
        rnd.score_differential(current_handicap_index)[0] for rnd in rounds.values()
    ]
    handicap_index = round(sum(score_diffs) / len(score_diffs), 2)
    # update_user_handicap(user_id)
    breakpoint()
    return handicap_index


def add_new_round(user_id: str, round: Round):
    diff = 2
    exceptional_adjustment(diff)
    pass


if __name__ == "__main__":
    calculate_handicap_index("")
