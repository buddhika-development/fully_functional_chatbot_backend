from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse
import src.repository as repo
from src.handlers.chat.chat_handler import handle_structured_response, handle_stream_response, access_chat_session_conversation_history

from pydantic import BaseModel

class ChatRequestBody(BaseModel):
    chat_session_id : str | None = None
    user_message : str = ""

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
)

@router.post("/structure")
async def _structured_chat_handler(req: ChatRequestBody):
    return  await handle_structured_response(
        session_id= req.chat_session_id,
        user_message= req.user_message
    )

@router.post("/stream")
async def _stream_chat_handler(req: ChatRequestBody):
    return StreamingResponse(
        handle_stream_response(user_message=req.user_message, session_id= req.chat_session_id),
        status_code=status.HTTP_200_OK,
        media_type= "text/event-stream"
    )

@router.get("/{id}")
async def _get_session_conversation_history(id: str):
    return await access_chat_session_conversation_history(session_id= id)