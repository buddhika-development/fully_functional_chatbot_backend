from langchain_core.prompts import PromptTemplate
import src.repository as repo
from pydantic import BaseModel, Field

class ChatSessionTitleOutput(BaseModel):
    title: str = Field(..., description= "Title for the conversation")

prompt_message = """
    role : session title writer
    goal : write small 5,6 words title for the conversation.
    goal explanation : you needs to write the goal with the 5,6 words to relavent to the user message shared.
    
    output crieteria: write in the plain text format dont use markdown format. don't use * marks and other notations comes in the markdown format.
    
    user_message :{user_message}
"""

async def generate_session_title(message: str) :
    prompt_template = PromptTemplate.from_template(prompt_message)
    llm = repo.mistral_structured_model
    title_llm = llm.with_structured_output(ChatSessionTitleOutput)
    prompt = prompt_template.invoke({
        "user_message" : message
    })
    response = title_llm.invoke(prompt)

    return response.title