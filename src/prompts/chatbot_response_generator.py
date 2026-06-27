from langchain_core.prompts import PromptTemplate
from src.db_actions.conversation import get_chat_session_conversation
from src.db_actions.chat_session import get_chat_session_summery

prompt_message = """
    you needs to act as professional assistant. You needs to understand about what is the user intent and provide friendly response to the user based on the user messsage. to generate response you can use the past conversations for understand the situations, you can use chat session summery for get understanding about what's happing during the conversation to provide answer to user message.
    
    chat_session_summary:
    {chat_session_summary}
    
    past_conversation:
    {past_conversation}
    
    user_message: 
    {user_message}
"""

def format_conversation_history(conversations) -> str:
    """Convert conversation objects into a formatted string."""
    lines = []
    for conv in conversations:
        role = conv.role.capitalize()  # "user" → "User"
        content = conv.content
        lines.append(f"{role}: {content}")
    return "\n".join(lines)

async def chat_response_generator_prompt(
        user_message: str,
        session_id: str
) :
    # retrieve the most recent 6 session messages
    past_conversations = await get_chat_session_conversation(
        session_id= session_id,
        limit= 6
    )

    str_past_conversations = format_conversation_history(past_conversations)
    chat_session_summary = await get_chat_session_summery(session_id)

    prompt_template = PromptTemplate.from_template(prompt_message)

    return prompt_template.invoke({
        "past_conversation": str_past_conversations,
        "user_message": user_message,
        "chat_session_summary": chat_session_summary
    })