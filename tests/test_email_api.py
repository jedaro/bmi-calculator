import app.api.endpoints.bmi as bmi_endpoint
from app.core.config import SmtpSettings


def configured_settings():
    return SmtpSettings(
        host="smtp.example.com",
        port=587,
        security="starttls",
        username="user",
        password="password",
        sender="sender@example.com",
        timeout_seconds=10,
    )


def test_email_delivery_acceptance(client, monkeypatch):
    monkeypatch.setattr(
        bmi_endpoint,
        "get_smtp_settings",
        configured_settings,
    )
    monkeypatch.setattr(bmi_endpoint, "send_email", lambda *args: None)

    response = client.post(
        "/api/v1/bmi/send-email",
        json={"email": "person@example.com", "weight": 75, "height": 1.75},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
    assert "bandeja" in response.json()["message"]


def test_invalid_email_is_rejected(client):
    response = client.post(
        "/api/v1/bmi/send-email",
        json={"email": "invalid", "weight": 75, "height": 1.75},
    )

    assert response.status_code == 422


def test_missing_email_configuration(client, monkeypatch):
    monkeypatch.setattr(
        bmi_endpoint,
        "get_smtp_settings",
        lambda: SmtpSettings(None, 587, "", None, None, None, 10),
    )

    response = client.post(
        "/api/v1/bmi/send-email",
        json={"email": "person@example.com", "weight": 75, "height": 1.75},
    )

    assert response.status_code == 503
    assert "password" not in response.text


def test_email_delivery_failure(client, monkeypatch):
    monkeypatch.setattr(
        bmi_endpoint,
        "get_smtp_settings",
        configured_settings,
    )

    def fail(*args):
        raise bmi_endpoint.MailDeliveryError("smtp details")

    monkeypatch.setattr(bmi_endpoint, "send_email", fail)

    response = client.post(
        "/api/v1/bmi/send-email",
        json={"email": "person@example.com", "weight": 75, "height": 1.75},
    )

    assert response.status_code == 502
    assert "smtp" not in response.text.lower()
