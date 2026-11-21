def test_application_documentation_is_available(client):
    response = client.get("/docs")

    assert response.status_code == 200

    openapi_response = client.get("/openapi.json")
    assert openapi_response.status_code == 200
    assert openapi_response.json()["info"]["title"] == "BMI Calculator API"
