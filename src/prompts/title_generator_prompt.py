from langchain_core.prompts import PromptTemplate

chat_prompt_message = """
    You needs to act as professional title writer. Your goal is write the title for the session based on the user initial message. You needs to understand about the domain about the chat will move forward. After that you needs to prepare the title for the conversation. And you needs to stick to the role. YOu needs to generate title in between 4 to 6 words.
    
    user_message : {user_message}
"""

def chat_session_title_prompt_template(user_message: str):
    prompt_template = PromptTemplate.from_template(chat_prompt_message)
    return prompt_template.invoke({
        "user_message": user_message
    })