from __future__ import annotations

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(PydanticBaseModel):
    # TODO[pydantic]: The following keys were removed: `underscore_attrs_are_private`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(use_enum_values=True)
