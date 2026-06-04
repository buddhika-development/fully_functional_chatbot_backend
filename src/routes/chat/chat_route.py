from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
)

@router.post("/stream")
async def _stream_chat_handler():
    return {
        "status": "success",
        "message" : "this is chat streaming router"
    }

@router.post("/structured")
async def _structured_chat_handler():
    return {
        "status": "success",
        "message" : "this is chat structured router"
    }