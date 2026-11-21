import smtplib
import ssl
from email.message import EmailMessage

from app.core.config import SmtpSettings
from app.services.bmi_service import calculate_bmi


class MailDeliveryError(Exception):
    pass


def build_email_message(
    recipient: str,
    sender: str,
    weight: float,
    height: float,
) -> EmailMessage:
    result = calculate_bmi(weight, height)
    message = EmailMessage()
    message["Subject"] = "Resultado de IMC"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(
        "Hola,\n\n"
        f"Peso: {weight} kg\n"
        f"Altura: {height} m\n"
        f"IMC: {result.bmi}\n"
        f"Categoria: {result.category}\n\n"
        "Este resultado es informativo y no constituye un diagnostico medico."
    )
    return message


def send_email(
    recipient: str,
    weight: float,
    height: float,
    settings: SmtpSettings,
) -> None:
    if not settings.host or not settings.sender:
        raise MailDeliveryError("Mail delivery is not configured")

    message = build_email_message(
        recipient,
        settings.sender,
        weight,
        height,
    )

    try:
        context = ssl.create_default_context()
        if settings.security == "ssl":
            client = smtplib.SMTP_SSL(
                settings.host,
                settings.port,
                timeout=settings.timeout_seconds,
                context=context,
            )
        else:
            client = smtplib.SMTP(
                settings.host,
                settings.port,
                timeout=settings.timeout_seconds,
            )

        with client:
            if settings.security == "starttls":
                client.starttls(context=context)
            if settings.username:
                client.login(settings.username, settings.password or "")
            client.send_message(message)
    except (smtplib.SMTPException, OSError, ssl.SSLError) as exc:
        raise MailDeliveryError("Mail delivery failed") from exc
