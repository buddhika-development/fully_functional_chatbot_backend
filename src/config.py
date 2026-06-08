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

config = Config()