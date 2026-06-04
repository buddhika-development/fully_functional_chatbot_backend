from fastapi import FastAPI
from src.routes.health.health_route import router as health_router

app = FastAPI()

app.include_router(health_router)