import pytest


def test_calculate_bmi_endpoint(client):
    response = client.post(
        "/api/v1/bmi/calculate",
        json={"weight": 75, "height": 1.75},
    )

    assert response.status_code == 200
    assert response.json() == {
        "weight": 75,
        "height": 1.75,
        "bmi": 24.49,
        "category": "Peso normal",
    }


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"weight": "not-a-number", "height": 1.75},
        {"weight": 75, "height": "not-a-number"},
        {"weight": 0, "height": 1.75},
        {"weight": -1, "height": 1.75},
        {"weight": 75, "height": 0},
        {"weight": 75, "height": -1},
    ],
)
def test_calculate_bmi_rejects_invalid_payload(client, payload):
    response = client.post("/api/v1/bmi/calculate", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "body",
    [
        '{"weight":1e999,"height":1.75}',
        '{"weight":75,"height":1e999}',
    ],
)
def test_calculate_bmi_rejects_non_finite_json(client, body):
    response = client.post(
        "/api/v1/bmi/calculate",
        content=body,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422
