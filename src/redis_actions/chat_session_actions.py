import src.repository as repo
from src.config import config
import json

async def load_recent_session_conversations(session_id: str) :
    conversation_key = config.redis_session_conversation_key.format(session_id=session_id)
    messages = await repo.async_redis_client.lrange(conversation_key, 0, -1)
    return messages

async def update_recent_session_conversations(session_id: str, human_message, ai_message) :
    human_msg_str = json.dumps(human_message) if isinstance(human_message, dict) else human_message
    ai_msg_str = json.dumps(ai_message) if isinstance(ai_message, dict) else ai_message

    conversation_key = config.redis_session_conversation_key.format(session_id=session_id)
    pipeline = repo.async_redis_client.pipeline()

    pipeline.rpush(conversation_key, human_msg_str, ai_msg_str)
    pipeline.ltrim(conversation_key, -4, -1)

    pipeline.expire(conversation_key, config.session_ttl)
    await pipeline.execute()

async def load_session_summery(session_id: str) :
    summery_key = config.redis_session_summery_key.format(session_id=session_id)
    summery = await repo.async_redis_client.get(summery_key)
    return summery

async def update_session_summery(session_id: str, session_summery: str) :
    summery_key = config.redis_session_summery_key.format(session_id=session_id)
    pipeline = repo.async_redis_client.pipeline()
    pipeline.set(summery_key, session_summery)

    pipeline.expire(summery_key, config.session_ttl)
    await pipeline.execute()


async def load_session_information(session_id: str) :
    await load_session_summery(session_id)
    await load_recent_session_conversations(session_id)