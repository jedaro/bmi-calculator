import math
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class BmiCalculation:
    weight: float
    height: float
    bmi: float
    category: Literal["Bajo peso", "Peso normal", "Sobrepeso", "Obesidad"]


def calculate_bmi(weight: float, height: float) -> BmiCalculation:
    if not math.isfinite(weight) or weight <= 0:
        raise ValueError("El peso debe ser un numero finito mayor que 0")
    if not math.isfinite(height) or height <= 0:
        raise ValueError("La altura debe ser un numero finito mayor que 0")

    bmi = weight / (height * height)
    if bmi < 18.5:
        category = "Bajo peso"
    elif bmi < 25:
        category = "Peso normal"
    elif bmi < 30:
        category = "Sobrepeso"
    else:
        category = "Obesidad"

    return BmiCalculation(
        weight=weight,
        height=height,
        bmi=round(bmi, 2),
        category=category,
    )
