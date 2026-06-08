from langchain_mistralai import ChatMistralAI
from src.config import config
import logging

logger = logging.getLogger("uvicorn.error")

def load_mistral_structured_model(
        model_name : str = config.mistral_default_model,
        temperature : float = config.default_model_temperature
):
    try:
        llm = ChatMistralAI(
            api_key= config.mistral_api_key,
            model = model_name,
            temperature= temperature
        )

        logger.info(f"Successfully mistral loaded structured model: {model_name}")
        return llm
    except Exception as e:
        logger.error(f"Something went wrong while mistral loading model: {e}")
        raise Exception(f"Something went wrong.. {e}")


def load_mistral_stream_model(
        model_name : str = config.mistral_default_model,
        temperature : float = config.default_model_temperature
):
    try:
        llm = ChatMistralAI(
            api_key= config.mistral_api_key,
            model = model_name,
            temperature= temperature,
            streaming= True
        )

        logger.info(f"Successfully mistral loaded stream model: {model_name}")
        return llm
    except Exception as e:
        logger.error(f"Something went wrong while mistral loading model: {model_name}")
        raise Exception(f"Something went wrong.. {e}")