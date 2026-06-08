import logging
from sqlalchemy import create_engine, text
from src.config import config

logger = logging.getLogger("uvicorn.error")

def get_engine():
    try:
        engine = create_engine(
            config.DATABASE_URL,
            echo=True,
        )

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            
        logger.info("Successfully execute the database engine connection verification process")
        return engine
    except Exception as e:
        logger.error(f"Something went wrong in the database connection process : {e}")
        raise

