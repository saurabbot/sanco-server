from typing import Any
from fastapi import APIRouter, Depends, Request
from redis.asyncio import Redis

from app import schemas
from app.core.redis import get_redis
from app.services.chatbot import chatbot_service
from app.services.chat_memory import ChatMemoryService

router = APIRouter()

@router.post("/message", response_model=schemas.ChatResponse)
async def chat_with_bot(
    request_data: schemas.ChatRequest,
    request: Request,
    redis: Redis = Depends(get_redis)
) -> Any:
    # 1. Identify user (Scalable: using IP or Session Header)
    client_ip = request.client.host
    
    memory = ChatMemoryService(redis)
    
    # 2. Add user message to memory
    await memory.add_message(client_ip, "user", request_data.message)
    
    # Retrieve context window for the LLM from Redis
    history = await memory.get_messages(client_ip)
    
    # Use ChatBotService with RAG
    bot_response = await chatbot_service.get_answer(request_data.message, history)
    
    # 4. Add bot response to memory
    await memory.add_message(client_ip, "assistant", bot_response)
    
    return {
        "response": bot_response,
        "context_length": len(history) + 1
    }

@router.delete("/clear")
async def clear_chat(request: Request, redis: Redis = Depends(get_redis)):
    client_ip = request.client.host
    memory = ChatMemoryService(redis)
    await memory.clear_memory(client_ip)
    return {"status": "cleared", "ip": client_ip}
