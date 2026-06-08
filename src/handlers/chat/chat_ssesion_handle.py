from src.db_actions.chat_session import get_user_chat_sesssions, delete_chat_session

async def access_use_chat_sesion(
    user_id: str
):
    sessions = await get_user_chat_sesssions(user_id)
    return {
        "status" : "success",
        "message" : "successfully access the user chat sessions",
        "data" : sessions
    }

async def delete_user_chat_session(
    user_id: str,
    session_id: str
):
    session = await delete_chat_session(user_id, session_id)
    return {
        "status" : "success",
        "message" : "successfully delete the user chat session",
        "data" : session
    }