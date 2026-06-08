from sqlalchemy import select, delete
import src.repository as repo
from src.models.chat_session import ChatSession

async def create_chat_session(
        user_id: str
):
    with repo.postgres() as conn:
        new_session = ChatSession(
            user_id = user_id
        )
        conn.add(new_session)
        conn.commit()
        conn.refresh(new_session)

        return new_session

async def update_chat_session_title(
        chat_session_id : str,
        session_title: str
):
    with repo.postgres() as conn:
        stmt = select(ChatSession).where(ChatSession.id == chat_session_id)
        chat_session = conn.execute(stmt).scalar_one_or_none()

        if chat_session is None:
            raise Exception("Chat session not found")

        chat_session.session_title = session_title
        conn.commit()
        conn.refresh(chat_session)

        return chat_session

async def get_user_chat_sesssions(user_id: str) :
    with repo.postgres() as conn:
        stmt = select(ChatSession).where(ChatSession.user_id == user_id)
        chat_session = conn.execute(stmt).scalars().all()

        return chat_session

async def delete_chat_session(user_id: str, session_id: str):
    with repo.postgres() as conn:
        stmt = delete(ChatSession).where(ChatSession.user_id == user_id, ChatSession.id == session_id)
        result = conn.execute(stmt)
        conn.commit()

        return session_id