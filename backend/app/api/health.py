from fastapi import APIRouter
from app.schemas.health import HealthStatus
from app.services.health import get_health_status

router = APIRouter()

@router.get("/health", response_model=HealthStatus)
def health():
    return get_health_status()