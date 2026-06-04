import logging
from sqlalchemy import create_engine
from src.config import config

logger = logging.getLogger("uvicorn.error")

def get_engine():
    try:
        return create_engine(
            config.DATABASE_URL,
            echo=True,
        )
    except Exception as e:
        logger.error(f"Something went wrong in the database connection process : {e}")
        raise

