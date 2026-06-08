from src.db_actions.chat_session import create_chat_session, update_chat_session_title
from src.controller.ai_controllers.title_generator import generate_session_title

async def create_new_chat_session(
        user_id: str,
        user_message: str
):
    chat_session = await create_chat_session(
        user_id= user_id
    )
    title = await generate_session_title(user_message)
    chat_session = await update_chat_session_title(chat_session.id, title)
    return chat_session

