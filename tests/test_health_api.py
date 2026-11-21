def test_api_availability(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"status": "available"}


def test_application_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
