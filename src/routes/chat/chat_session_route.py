from fastapi import APIRouter
from src.handlers.chat.chat_ssesion_handle import access_use_chat_sesion, delete_user_chat_session

router = APIRouter(
    prefix="/api/v1/chat_session",
    tags=["chat_session"]
)

dummy_user_id = "40515f81-57b0-4f02-b33d-512f18e968b2"

@router.get("/me")
async def _get_user_chat_session():
    return await access_use_chat_sesion(dummy_user_id)

@router.delete("/{chat_session_id}")
async def _delete_chat_session(chat_session_id: str):
    return await delete_user_chat_session(dummy_user_id ,chat_session_id)