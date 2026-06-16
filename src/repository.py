import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.libs.postgres.database import get_engine, get_async_engine
from sqlalchemy.orm import sessionmaker
from src.libs.llm.mistral import load_mistral_structured_model, load_mistral_stream_model
from src.libs.redis.redis import get_redis_client
import redis

logger = logging.getLogger("uvicorn.error")

engine = None
postgres = None
async_engine = None
async_postgres = None
mistral_structured_model = None
mistral_stream_model = None
redis_client = None

def repository_init():
    global engine, postgres, mistral_structured_model, mistral_stream_model, async_engine, async_postgres, mistral_structured_model, mistral_stream_model, redis_client

    try:
        engine = get_engine()
        postgres = sessionmaker(
            bind=engine,
            autoflush= False,
            autocommit= False
        )
        logger.info("Successfully connected to PostgreSQL database")

        async_engine = get_async_engine()
        async_postgres = async_sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            autoflush= False,
            autocommit= False,
            expire_on_commit= False
        )

        mistral_structured_model = load_mistral_structured_model()
        mistral_stream_model = load_mistral_stream_model()

        redis_pool = get_redis_client()
        redis_client = redis.Redis(connection_pool=redis_pool)
        logger.info("Successfully connected the redis client.")

        logger.info("Successfully execute the repository initialization process.")
    except Exception as e:
        logger.error(f"Something went wrong while repository initialization process: {e}")
        raise
