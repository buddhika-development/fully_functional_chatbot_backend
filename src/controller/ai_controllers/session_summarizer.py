import src.repository as repo
from langchain_core.prompts import PromptTemplate
from src.db_actions.chat_session import get_chat_session_summery, update_chat_session_summery
import src.redis_actions.chat_session_actions as redis
import json

prompt_message = """
    you needs to act as the conversation summary write. your job is write the valueble summary for the conversation based on the current summary and the new set of conversations.
    
    current_summary:
    {current_summary}
    
    new_conversations:
    {new_conversations}
"""

prompt_template = PromptTemplate.from_template(prompt_message)

async def chat_session_summarizer(chat_session_id: str):
    # take the current summary from the database
    # generate the new summery
    # update the database and the redis layer
    chat_session_summery = await redis.load_session_summery(chat_session_id)

    conversations = await redis.load_recent_session_conversations(chat_session_id)
    parsed_messages = [json.loads(msg) if isinstance(msg, str) else msg for msg in conversations]
    formatted_transcript = ""
    for msg in parsed_messages:
        # Capitalize the role to make it clear for the LLM
        role = "User" if msg.get("role") == "user" else "AI"
        content = msg.get("content", "")

        formatted_transcript += f"{role}: {content}\n"

    prompt = prompt_template.invoke({
        "current_summary" : chat_session_summery,
        "new_conversations" : formatted_transcript
    })
    response = repo.mistral_structured_model.invoke(prompt)

    await redis.update_session_summery(
        session_id = chat_session_id,
        session_summery=response.content
    )
    db_response = await update_chat_session_summery(chat_session_id, response.content)