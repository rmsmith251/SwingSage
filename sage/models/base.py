from __future__ import annotations

import math

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field


class BaseModel(PydanticBaseModel):
    # TODO[pydantic]: The following keys were removed: `underscore_attrs_are_private`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(use_enum_values=True)


class Coordinates(BaseModel):
    latitude: float
    longitude: float

    def to_string(self) -> str:
        return f"{self.latitude},{self.longitude}"

    @property
    def latitude_radians(self) -> float:
        return self.latitude * math.pi / 180

    @property
    def longitude_radians(self) -> float:
        return self.longitude * math.pi / 180


class MeasuredValue(BaseModel):
    value: float
    unit: str = Field(..., validation_alias="unitCode")
