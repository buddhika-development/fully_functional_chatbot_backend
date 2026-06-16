from src.config import config
import redis
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