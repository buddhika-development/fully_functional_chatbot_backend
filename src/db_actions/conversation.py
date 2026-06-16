from sqlalchemy import select, desc, func

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

async def get_chat_session_conversation(
        session_id:str,
        limit: int = 10,
        skip: int = 0
) :
    stmt = (
        select(Conversation)
        .where(Conversation.session_id == session_id)
        .order_by(desc(Conversation.created_at))
        .offset(skip)
        .limit(limit)
    )

    async with repo.async_postgres() as conn:
        result = await conn.execute(stmt)
        conversations = result.scalars().all()
        return list(reversed(conversations))

async def get_the_conversation_turn_count(
        session_id: id
):
    stmt = (
        select(func.count())
        .select_from(Conversation)
        .where(Conversation.session_id == session_id)
    )

    with repo.postgres() as conn:
        execution_result = conn.execute(stmt)
        result = execution_result.scalar_one()
        return result