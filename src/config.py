import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL= os.getenv("DATABASE_URL")

    # ai configurations
    default_model_temperature = 1.0

    # mistral configurations
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    mistral_default_model = os.getenv("MISTRAL_DEFAULT_MODEL")

    # redis configuration
    redis_host = os.getenv("REDIS_HOST")
    redis_port = os.getenv("REDIS_PORT")
    redis_password = os.getenv("REDIS_PASSWORD")
    redis_db_index = os.getenv("REDIS_DATABASE_INDEX")

    redis_session_conversation_key = "session:{session_id}:messages"
    redis_session_summery_key = "session:{session_id}:summery"
    session_ttl = 1800

config = Config()