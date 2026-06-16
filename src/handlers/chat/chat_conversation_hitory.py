from src.db_actions.conversation import (
    get_chat_session_conversation,
)

async def access_chat_session_conversation_history(session_id: str, limit: int = 10, skip: int = 0):
    conversation = await get_chat_session_conversation(session_id, limit, skip)
    return {
        "status": "success",
        "message": "Successfully generated the conversation history.",
        "data": conversation,
    }
