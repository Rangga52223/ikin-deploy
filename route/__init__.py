from fastapi import APIRouter

test = APIRouter(
    prefix="/api/v1/test",
    tags=["test"]
)

need = APIRouter(
    prefix="/api/v1/need",
    tags=["uploads"]
)

serve = APIRouter(
    prefix="/api/v1/telemetry",
    tags=["serve telemetry"]
)

authen = APIRouter(
    prefix="/api/v1/analysis",
    tags=["Telemetry Analysis"]
)