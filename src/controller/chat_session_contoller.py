from src.db_actions.conversation import create_conversation, get_the_conversation_turn_count
from src.controller.ai_controllers.session_summarizer import chat_session_summarizer

async def chat_session_conversation_handler(
        session_id: str,
        user_message: str,
        ai_response: str,
):
    # save the message conversations in the database
    user_conversation = await create_conversation(
        session_id=session_id,
        role="human",
        content=user_message,
        additional_info=None
    )
    system_conversation = await create_conversation(
        session_id=session_id,
        role="assistant",
        content=ai_response,
        additional_info=None
    )
    conversations = [{
        "role": "human",
        "content": user_message
    }, {
        "role": "assistant",
        "content": ai_response
    }]

    conversation_turn_count = await get_the_conversation_turn_count(session_id)
    if conversation_turn_count >= 4:
        await chat_session_summarizer(
            chat_session_id=session_id,
            conversation=conversations
        )