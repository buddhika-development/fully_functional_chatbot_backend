import logging
from src.libs.postgres.database import get_engine
from sqlalchemy.orm import sessionmaker
from src.libs.llm.mistral import load_mistral_structured_model, load_mistral_stream_model

logger = logging.getLogger("uvicorn.error")

engine = None
postgres = None
mistral_structured_model = None
mistral_stream_model = None

def repository_init():
    global engine, postgres, mistral_structured_model, mistral_stream_model

    try:
        engine = get_engine()
        postgres = sessionmaker(
            bind=engine,
            autoflush= False,
            autocommit= False
        )
        logger.info("Successfully connected to PostgreSQL database")

        mistral_structured_model = load_mistral_structured_model()
        mistral_stream_model = load_mistral_stream_model()

        logger.info("Successfully execute the repository initialization process.")
    except Exception as e:
        logger.error(f"Something went wrong while repository initialization process: {e}")
        raise
