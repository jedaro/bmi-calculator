from app.core.config import SmtpSettings
from app.services.email_service import build_email_message, send_email


def test_email_message_contains_required_elements():
    message = build_email_message(
        recipient="person@example.com",
        sender="sender@example.com",
        weight=75,
        height=1.75,
    )

    body = message.get_content()
    assert "Hola" in body
    assert "75" in body
    assert "1.75" in body
    assert "24.49" in body
    assert "Peso normal" in body
    assert "informativo" in body


class FakeSMTP:
    def __init__(self, *args, **kwargs):
        self.started_tls = False
        self.logged_in = False
        self.sent_message = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def starttls(self, context=None):
        self.started_tls = True

    def login(self, username, password):
        self.logged_in = True

    def send_message(self, message):
        self.sent_message = message


def test_send_email_supports_starttls(monkeypatch):
    clients = []

    def smtp_factory(*args, **kwargs):
        client = FakeSMTP(*args, **kwargs)
        clients.append(client)
        return client

    monkeypatch.setattr("app.services.email_service.smtplib.SMTP", smtp_factory)
    settings = SmtpSettings(
        host="smtp.example.com",
        port=587,
        security="starttls",
        username="user",
        password="password",
        sender="sender@example.com",
        timeout_seconds=10,
    )

    send_email("person@example.com", 75, 1.75, settings)

    assert clients[0].started_tls
    assert clients[0].logged_in
    assert clients[0].sent_message is not None


def test_send_email_supports_ssl(monkeypatch):
    clients = []

    def smtp_ssl_factory(*args, **kwargs):
        client = FakeSMTP(*args, **kwargs)
        clients.append(client)
        return client

    monkeypatch.setattr("app.services.email_service.smtplib.SMTP_SSL", smtp_ssl_factory)
    settings = SmtpSettings(
        host="smtp.example.com",
        port=465,
        security="ssl",
        username=None,
        password=None,
        sender="sender@example.com",
        timeout_seconds=10,
    )

    send_email("person@example.com", 75, 1.75, settings)

    assert clients[0].sent_message is not None
