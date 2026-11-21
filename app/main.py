from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.endpoints.bmi import router as bmi_router
from app.api.endpoints.health import router as health_router


app = FastAPI(
    title="BMI Calculator API",
    version="1.0.0",
)

app.include_router(bmi_router)
app.include_router(health_router)
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    detail = []
    for error in exc.errors():
        detail.append(
            {
                "loc": error["loc"],
                "msg": error["msg"],
                "type": error["type"],
            }
        )
    return JSONResponse(status_code=422, content={"detail": detail})
