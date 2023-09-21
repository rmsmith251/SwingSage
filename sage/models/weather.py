from __future__ import annotations

import json
from enum import Enum

import requests
from pydantic import AliasPath, Field, TypeAdapter

from sage.models.base import BaseModel, Coordinates, MeasuredValue
from sage.utils.logging import get_logger
from sage.utils.misc import distance_between_coordinates_miles
from sage.utils.settings import Settings

settings = Settings()
logger = get_logger(settings.log_level)

# The following header is for accountability with NWS. Until this is a deployed service for the public, anyone using
# this will need to use their own name and email.
HEADERS = {
    "User-Agent": json.dumps(
        {
            "app": "SwingSage",
            "user": settings.user,
            "email": settings.contact_email,
            "app-version": "0.0.1",
        }
    )
}


class NWSURLEnum(str, Enum):
    points = "https://api.weather.gov/points"
    zone_stations = "https://api.weather.gov/zones/forecast/{zone_id}/stations"


class WeatherData(BaseModel):
    id: str
    text_description: str = Field(
        ..., validation_alias=AliasPath("properties", "textDescription")
    )
    temperature: MeasuredValue = Field(
        ..., validation_alias=AliasPath("properties", "temperature")
    )
    wind_direction: MeasuredValue = Field(
        ..., validation_alias=AliasPath("properties", "windDirection")
    )
    wind_speed: MeasuredValue = Field(
        ..., validation_alias=AliasPath("properties", "windSpeed")
    )
    heat_index: MeasuredValue = Field(
        ..., validation_alias=AliasPath("properties", "heatIndex")
    )


class Station(BaseModel):
    id: str
    url: str
    latitude: float = Field(
        ..., validation_alias=AliasPath("geometry", "coordinates", 1)
    )
    longitude: float = Field(
        ..., validation_alias=AliasPath("geometry", "coordinates", 0)
    )
    elevation: MeasuredValue = Field(
        ..., validation_alias=AliasPath("properties", "elevation")
    )
    station_id: str = Field(
        ..., validation_alias=AliasPath("properties", "stationIdentifier")
    )
    name: str = Field(..., validation_alias=AliasPath("properties", "name"))

    _location: Coordinates | None = None

    @property
    def location(self) -> Coordinates:
        if self._location is None:
            self._location = Coordinates(
                latitude=self.latitude, longitude=self.longitude
            )
        return self._location

    def distance(self, loc: Coordinates) -> float:
        """
        Returns the true distance between points in miles
        """
        return distance_between_coordinates_miles(self.location, loc)

    def latest_observation(self) -> WeatherData:
        response = requests.get(f"{self.url}/observations/latest", headers=HEADERS)
        response.raise_for_status()
        breakpoint()
        return WeatherData(**response.json())

    @classmethod
    def from_url(self, url: str) -> Station:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return Station(url=url, **response.json())


class PointMetaData(BaseModel):
    cwa: str
    office: str = Field(..., validation_alias="forecastOffice")
    grid_id: str = Field(..., validation_alias="gridId")
    grid_x: int = Field(..., validation_alias="gridX")
    grid_y: int = Field(..., validation_alias="gridY")
    forecast_office: str = Field(..., validation_alias="forecastOffice")
    forecast: str
    hourly_forecast: str = Field(..., validation_alias="forecastHourly")
    forecast_grid_data: str = Field(..., validation_alias="forecastGridData")
    observation_stations: str = Field(..., validation_alias="observationStations")
    forecast_zone: str = Field(..., validation_alias="forecastZone")
    radar_station: str = Field(..., validation_alias="radarStation")


class NWS(BaseModel):
    location: Coordinates
    limit: int = 100

    _point: PointMetaData | None = None
    _station: Station | None = None
    _distance: float = 9e9
    _current_weather: WeatherData | None = None
    _last_hole: int = 0

    @property
    def point(self) -> PointMetaData:
        if self._point is None:
            response = requests.get(
                f"{NWSURLEnum.points.rstrip('/')}/{self.location.to_string()}",
                headers=HEADERS,
            )
            if response.status_code == 200:
                self._point = TypeAdapter(PointMetaData).validate_python(
                    response.json().get("properties", {})
                )
            else:
                logger.error(
                    f"Point error: Status Code: {response.status_code}, Response error: {response.json()}"
                )
        return self._point

    @property
    def station(self) -> Station | None:
        if self._station is None:
            if self.limit > 500:
                logger.warning(
                    f"The limit is set to {self.limit} which is too high (max 500). Setting to 100"
                )
                self.limit = 100
            response = requests.get(self.point.forecast_office, headers=HEADERS)
            if response.status_code == 200:
                raw_stations = response.json().get("approvedObservationStations", [])
                stations = [
                    Station.from_url(station_url) for station_url in raw_stations
                ]
                dist, station = get_best_station(self.location, stations)
                if station is None:
                    logger.error("No station found")
                else:
                    logger.info(
                        f"Station {station.station_id} found with distance {dist}"
                    )
                    self._station = station
                    self._distance = dist
            else:
                logger.error(
                    f"Station error: Status Code: {response.status_code}, Response error: {response.json()}"
                )
        return self._station

    def current_weather(self, hole: int) -> WeatherData:
        """
        Get the weather for the hole that you're on. Only checks once per hole so that we aren't spamming the
        NWS API.
        """
        if self._current_weather is None or hole > self._last_hole:
            self._current_weather = self.station.latest_observation()
            self._last_hole = hole
        return self._current_weather


def get_best_station(
    location: Coordinates, stations: list[Station]
) -> tuple[float, Station]:
    best_station: Station | None = None
    best_distance: float = 9e9
    for station in stations:
        dist = station.distance(location)
        logger.debug(f"Station: {station.name}, distance: {dist}")
        if dist < best_distance:
            best_distance = dist
            best_station = station

    return best_distance, best_station
