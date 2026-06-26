from src.config import config
import redis
import redis.asyncio as async_redis
import logging

logger = logging.getLogger("uvicorn.error")

def get_redis_client():
    pool = redis.ConnectionPool(
        host = config.redis_host,
        port = config.redis_port,
        db = config.redis_db_index,
        decode_responses = True
    )
    logger.info("Redis pool successfully initialized")
    return pool

def get_async_redis_client():
    pool = async_redis.ConnectionPool(
        host=config.redis_host,
        port=config.redis_port,
        db=config.redis_db_index,
        decode_responses=True
    )
    logger.info("Async redis pool successfully initialized")
    return pool