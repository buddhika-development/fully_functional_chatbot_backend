import json
from fastapi import HTTPException
from fastapi import APIRouter, HTTPException, status
import src.repository as repo
import logging
from src.controller.chat_controller import create_new_chat_session
from src.controller.chat_session_contoller import chat_session_conversation_handler
from src.db_actions.conversation import (
    create_conversation,
    get_chat_session_conversation,
)
from src.controller.ai_controllers.session_summarizer import chat_session_summarizer
from src.prompts.chatbot_response_generator import chat_response_generator_prompt
import asyncio

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


async def handle_stream_response(session_id: str = None, user_message: str = ""):
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
            session_id = chat_session.id
            yield f"event: session_id\ndata: {chat_session.id}\n\n"

        prompt = await chat_response_generator_prompt(user_message, session_id)

        response = ""
        async for chunk in repo.mistral_stream_model.astream(prompt):
            if chunk:
                response += chunk.content
                # JSON-encode the chunk so newlines inside a token are escaped
                # (as \n) instead of leaking into the SSE framing. Without this,
                # a token containing a newline / blank line corrupts the
                # event boundaries and the client loses all line breaks while
                # streaming. See chat_session_route proxy + ChatContext parser.
                yield f"data: {json.dumps({'content': chunk.content})}\n\n"

        asyncio.create_task(
            chat_session_conversation_handler(
                session_id=session_id, user_message=user_message, ai_response=response
            )
        )
        yield f"data: [Done]\n\n"

    except TimeoutError:
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


async def access_chat_session_conversation_history(session_id: str, limit: int = 10, skip: int = 0):
    conversation = await get_chat_session_conversation(session_id, limit, skip)
    return {
        "status": "success",
        "message": "Successfully generated the conversation history.",
        "data": conversation,
    }
