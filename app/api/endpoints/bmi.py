from fastapi import APIRouter, HTTPException, status

from app.core.config import get_smtp_settings, smtp_is_configured
from app.schemas.bmi import BmiInput, BmiResult
from app.schemas.email import EmailRequest, EmailResponse
from app.services.bmi_service import calculate_bmi
from app.services.email_service import MailDeliveryError, send_email


router = APIRouter(prefix="/api/v1/bmi", tags=["BMI"])


@router.post("/calculate", response_model=BmiResult)
def calculate(payload: BmiInput) -> BmiResult:
    result = calculate_bmi(payload.weight, payload.height)
    return BmiResult(**result.__dict__)


@router.post("/send-email", response_model=EmailResponse)
def send_bmi_email(payload: EmailRequest) -> EmailResponse:
    settings = get_smtp_settings()
    if not smtp_is_configured(settings):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="La entrega de correo no esta configurada.",
        )

    try:
        send_email(
            payload.email,
            payload.weight,
            payload.height,
            settings,
        )
    except MailDeliveryError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No fue posible entregar el correo.",
        )

    return EmailResponse(
        status="accepted",
        message="El servidor SMTP acepto el mensaje para entrega. No se confirma la recepcion en la bandeja.",
    )
