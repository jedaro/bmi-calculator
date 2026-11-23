import math

import pytest

from app.services.bmi_service import calculate_bmi


@pytest.mark.parametrize(
    ("weight", "height", "expected_bmi", "expected_category"),
    [
        (75, 1.75, 24.49, "Peso normal"),
        (50, 1.75, 16.33, "Bajo peso"),
        (18.5 * 1.75 * 1.75, 1.75, 18.5, "Peso normal"),
        (25 * 1.75 * 1.75, 1.75, 25.0, "Sobrepeso"),
        (30 * 1.75 * 1.75, 1.75, 30.0, "Obesidad"),
    ],
)
def test_calculate_bmi(weight, height, expected_bmi, expected_category):
    result = calculate_bmi(weight, height)

    assert result.bmi == expected_bmi
    assert result.category == expected_category


@pytest.mark.parametrize("weight", [0, -1, math.inf, -math.inf, math.nan])
def test_calculate_bmi_rejects_invalid_weight(weight):
    with pytest.raises(ValueError):
        calculate_bmi(weight, 1.75)


@pytest.mark.parametrize("height", [0, -1, math.inf, -math.inf, math.nan])
def test_calculate_bmi_rejects_invalid_height(height):
    with pytest.raises(ValueError):
        calculate_bmi(75, height)
