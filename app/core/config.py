import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class SmtpSettings:
    host: str | None
    port: int
    security: str
    username: str | None
    password: str | None
    sender: str | None
    timeout_seconds: float


def get_smtp_settings() -> SmtpSettings:
    try:
        port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError:
        port = 587

    try:
        timeout = float(os.getenv("SMTP_TIMEOUT_SECONDS", "10"))
    except ValueError:
        timeout = 10.0

    security = os.getenv("SMTP_SECURITY", "").lower()

    return SmtpSettings(
        host=os.getenv("SMTP_HOST") or None,
        port=port,
        security=security,
        username=os.getenv("SMTP_USERNAME") or None,
        password=os.getenv("SMTP_PASSWORD") or None,
        sender=os.getenv("SMTP_SENDER") or None,
        timeout_seconds=timeout,
    )


def smtp_is_configured(settings: SmtpSettings) -> bool:
    return bool(
        settings.host
        and settings.sender
        and settings.security in {"starttls", "ssl"}
    )
