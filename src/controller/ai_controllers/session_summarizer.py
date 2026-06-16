import src.repository as repo
from langchain_core.prompts import PromptTemplate
from src.db_actions.chat_session import get_chat_session_summery, update_chat_session_summery

prompt_message = """
    you needs to act as the conversation summary write. your job is write the valueble summary for the conversation based on the current summary and the new set of conversations.
    
    current_summary:
    {current_summary}
    
    new_conversations:
    {new_conversations}
"""

prompt_template = PromptTemplate.from_template(prompt_message)

async def chat_session_summarizer(chat_session_id: str, conversation: str):
    # take the current summary from the database
    # generate the new summery
    # update the database and the redis layer
    chat_session_summery = await get_chat_session_summery(chat_session_id)

    prompt = prompt_template.invoke({
        "current_summary" : chat_session_summery,
        "new_conversations" : conversation
    })
    response = repo.mistral_structured_model.invoke(prompt)
    db_response = await update_chat_session_summery(chat_session_id, response.content)