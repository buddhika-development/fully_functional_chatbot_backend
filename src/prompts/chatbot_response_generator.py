from langchain_core.prompts import PromptTemplate

prompt_message = """
    you needs to act as professional assistant. You needs to understand about what is the user intent and provide friendly response to the user based on the user messsage.
    
    user_message: 
    {user_message}
"""

def chat_response_generator_prompt(user_message: str) :
    prompt_template = PromptTemplate.from_template(prompt_message)
    return prompt_template.invoke({
        "user_message": user_message
    })