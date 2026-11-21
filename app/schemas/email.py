import math
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


def finite_positive(value: float) -> float:
    if not math.isfinite(value) or value <= 0:
        raise ValueError("Debe ser un numero finito mayor que 0")
    return value


class EmailRequest(BaseModel):
    model_config = {"extra": "forbid"}

    email: EmailStr
    weight: float = Field(gt=0)
    height: float = Field(gt=0)

    _validate_weight = field_validator("weight")(finite_positive)
    _validate_height = field_validator("height")(finite_positive)


class EmailResponse(BaseModel):
    model_config = {"extra": "forbid"}

    status: Literal["accepted"]
    message: str
