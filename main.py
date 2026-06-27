from fastapi import FastAPI
from src.repository import repository_init

from src.routes.health.health_route import router as health_router
from src.routes.chat.chat_route import router as chat_router
from src.routes.chat.chat_session_route import router as chat_session_router

app = FastAPI()
repository_init()

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(chat_session_router)