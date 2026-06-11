from langchain_core.prompts import PromptTemplate
import src.repository as repo
from pydantic import BaseModel, Field
from src.prompts.title_generator_prompt import chat_session_title_prompt_template

class ChatSessionTitleOutput(BaseModel):
    title: str = Field(..., description= "Title for the conversation")

async def generate_session_title(message: str) :
    prompt = chat_session_title_prompt_template(message)
    llm = repo.mistral_structured_model
    title_llm = llm.with_structured_output(ChatSessionTitleOutput)
    response = title_llm.invoke(prompt)

    return response.title