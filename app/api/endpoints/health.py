from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(tags=["Availability"])


class StatusResponse(BaseModel):
    status: str


@router.get("/", response_model=StatusResponse)
def api_availability() -> StatusResponse:
    return StatusResponse(status="available")


@router.get("/health", response_model=StatusResponse)
def application_health() -> StatusResponse:
    return StatusResponse(status="healthy")
