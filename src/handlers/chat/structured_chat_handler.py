import logging
import asyncio
from fastapi import HTTPException, status
import src.repository as repo
from src.controller.chat_controller import create_new_chat_session
from src.prompts.chatbot_response_generator import chat_response_generator_prompt
from src.controller.chat_session_contoller import chat_session_conversation_handler

logger = logging.getLogger("uvicorn.error")
dummy_user_id = "40515f81-57b0-4f02-b33d-512f18e968b2"

async def handle_structured_response(
    session_id: str | None = None, user_message: str = ""
):
    if not user_message or not user_message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user message cannot be empty.",
        )

    try:
        if session_id is None:
            chat_session = await create_new_chat_session(
                user_id=dummy_user_id, user_message=user_message
            )

        prompt = chat_response_generator_prompt(user_message)
        response = repo.mistral_structured_model.invoke(prompt)

        asyncio.create_task(
            chat_session_conversation_handler(
                session_id=session_id, user_message=user_message, ai_response=response
            )
        )

        return {
            "status": "success",
            "message": "Successfully generated the response",
            "data": {
                "session_id": chat_session.id,
                "session_title": chat_session.session_title,
                "content": response.content,
            },
        }

    except TimeoutError:
        logger.warning("Mistral AI model timed out.")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The AI model took too long to respond. Please try again.",
        )

    except Exception as e:
        logger.error(f"AI Generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request.",
        )
