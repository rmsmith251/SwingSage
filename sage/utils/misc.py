import math

from sage.models.base import Coordinates


def distance_between_coordinates_nautical_miles(
    coord1: Coordinates, coord2: Coordinates
) -> float:
    """
    Converted to Python from http://edwilliams.org/avform147.htm#Dist
    """
    lat_diff = coord1.latitude_radians - coord2.latitude_radians
    lon_diff = coord1.longitude_radians - coord2.longitude_radians
    lat_sin = math.sin(lat_diff / 2) ** 2
    lon_sin = math.sin(lon_diff / 2) ** 2
    cos_lat1 = math.cos(coord1.latitude_radians)
    cos_lat2 = math.cos(coord2.latitude_radians)
    final = lat_sin + cos_lat1 * cos_lat2 * lon_sin
    radians = 2 * math.asin(final**0.5)
    return radians * 180 * 60 / math.pi


def distance_between_coordinates_miles(
    coord1: Coordinates, coord2: Coordinates
) -> float:
    return distance_between_coordinates_nautical_miles(coord1, coord2) * 1.15078


def distance_between_coordinates_yards(
    coord1: Coordinates, coord2: Coordinates
) -> float:
    return distance_between_coordinates_miles(coord1, coord2) * 1760
