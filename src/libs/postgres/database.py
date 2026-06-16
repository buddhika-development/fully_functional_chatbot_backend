import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

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


def get_async_engine():
    try:
        async_connection_string = config.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        async_engine = create_async_engine(
            async_connection_string,
            echo=True,
            pool_size=20,
            max_overflow=10
        )

        logger.info("Successfully execute the database engine connection verification process")
        return async_engine
    except Exception as e:
        logger.error(f"Something went wrong in the database connection process : {e}")
        raise