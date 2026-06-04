from fastapi import FastAPI
from src.routes.health.health_route import router as health_router
from src.repository import repository_init

app = FastAPI()
repository_init()

app.include_router(health_router)