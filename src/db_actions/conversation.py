from sqlalchemy import select

from src.models.conversation import Conversation
import src.repository as repo

async def create_conversation(
        session_id: str,
        role: str,
        content: str,
        additional_info: dict | None
):
    with repo.postgres() as conn:
        conversation = Conversation(
            session_id = session_id,
            role = role,
            content = content,
            additional_information = additional_info
        )
        conn.add(conversation)
        conn.commit()
        conn.refresh(conversation)

        return conversation

async def get_chat_session_conversation(session_id:str) :
    stmt = select(Conversation).where(
        Conversation.session_id == session_id
    )

    with repo.postgres() as conn:
        result = conn.execute(stmt)
        conversations = result.scalars().all()
        return conversations