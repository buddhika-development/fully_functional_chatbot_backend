from src.libs.postgres.database import get_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger("uvicorn.error")

engine = None
postgres = None

def repository_init():
    global engine, postgres

    engine = get_engine()
    postgres = sessionmaker(
        bind=engine,
        autoflush= False,
        autocommit= False
    )
    logger.info("Successfully connected to PostgreSQL database")


