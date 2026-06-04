from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/chat_session",
    tags=["chat_session"]
)

@router.get("/me")
async def _get_user_chat_session():
    return {
        "status": "success",
        "message" : "this is chat session access process related to the user"
    }

@router.delete("/:chat_session_id")
async def _delete_chat_session(chat_session_id: str):
    return {
        "status": "success",
        "message" : "this is delete chat session access process related to the user"
    }