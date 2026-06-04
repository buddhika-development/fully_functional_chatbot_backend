from fastapi import APIRouter
from src.handlers.health.health_handler import initial_health_check

router = APIRouter(
    tags=["health"]
)

@router.get("/")
def _initial_health():
    return initial_health_check()