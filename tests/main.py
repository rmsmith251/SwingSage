import json

from pydantic import parse_obj_as

from sage.main import calculate_handicap_index, course_handicap, playing_handicap
from sage.utils.types import Rounds


def test_course_handicap():
    course_handicap(1, {})


def test_playing_handicap():
    playing_handicap("", {})


def test_calculate_handicap_index():
    with open("tests/assets/example_round.json", "r") as f:
        data = json.load(f)

    rounds = parse_obj_as(Rounds, data)
    handicap_index = calculate_handicap_index("test", rounds, -1.0)
    assert handicap_index == 12.38
