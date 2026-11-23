from fastapi import APIRouter, Depends
from src.handlers.chat.chat_ssesion_handle import access_use_chat_sesion, delete_user_chat_session
from src.utils.get_user import get_user_id_from_request

router = APIRouter(
    prefix="/api/v1/chat_session",
    tags=["chat_session"]
)

@router.get("/me")
async def _get_user_chat_session(
        user_id: str = Depends(get_user_id_from_request)
):
    return await access_use_chat_sesion(user_id)

@router.delete("/{chat_session_id}")
async def _delete_chat_session(
        chat_session_id: str,
        user_id: str = Depends(get_user_id_from_request)
):
    return await delete_user_chat_session(user_id ,chat_session_id)