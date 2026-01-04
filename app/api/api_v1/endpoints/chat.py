from typing import Any, List
from fastapi import APIRouter, Depends, Request, Response
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.core.redis import get_redis
from app.db.session import get_db
from app.services.chat_service import ChatService

router = APIRouter()

@router.get("/messages", response_model=List[dict])
async def get_chat_history(
    request: Request,
    response: Response,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
) -> Any:
    chat_service = ChatService(db, redis)
    session, _ = await chat_service.resolve_session(request, response)
    return await chat_service.get_history(session)


@router.post("/message", response_model=schemas.ChatResponse)
@router.post("/messages", response_model=schemas.ChatResponse, include_in_schema=False)
async def chat_with_bot(
    request_data: schemas.ChatRequest,
    request: Request,
    response: Response,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
) -> Any:
    chat_service = ChatService(db, redis)
    
    # 1. Resolve session from Body, Cookie, or Header
    session_uuid_input = request_data.session_uuid or request_data.sessionuuid
    session, session_uuid = await chat_service.resolve_session(request, response, session_uuid_input)
    
    # 2. Process chat
    return await chat_service.chat(session, session_uuid, request_data.message)


@router.delete("/clear")
async def clear_chat(
    request: Request, 
    response: Response, 
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_db),
):
    chat_service = ChatService(db, redis)
    _, session_uuid = await chat_service.resolve_session(request, response)
    
    if session_uuid:
        await chat_service.clear_chat(session_uuid)
    
    response.delete_cookie(ChatService.SESSION_COOKIE_NAME, path="/")
    return {"status": "cleared", "session_uuid": session_uuid}
