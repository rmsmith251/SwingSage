import pytest

from sage.models.base import Coordinates
from sage.utils.misc import distance_between_coordinates_yards


# To verify expected distances, use http://edwilliams.org/gccalc.htm and convert to yards.
# The real value will be stored as a float but I'm rounding to the nearest whole number for testing
@pytest.mark.parametrize(
    "coord1,coord2,expected",
    [
        (  # Hole 18 at Pebble Beach, tips to center of the green
            Coordinates(latitude=36.565530, longitude=-121.945201),
            Coordinates(latitude=36.567626, longitude=-121.949645),
            503,
        ),
        (  # LAX to JFK
            Coordinates(latitude=33.95, longitude=-118.4),
            Coordinates(latitude=40.633333, longitude=-73.783333),
            4341845,
        ),
        (  # Hole 16 at TPC Scottsdale, Stadium Course, from the tips
            Coordinates(latitude=33.637305, longitude=-111.914846),
            Coordinates(latitude=33.637442, longitude=-111.913281),
            159,
        ),
    ],
)
def test_distance_between_coordinates_yards(
    coord1: Coordinates, coord2: Coordinates, expected: int
):
    dist = distance_between_coordinates_yards(coord1, coord2)
    assert round(dist) == expected
