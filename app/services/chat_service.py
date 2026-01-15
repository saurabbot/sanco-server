import uuid
import time
from typing import Dict, Any, List
from fastapi import Request, Response, HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.chatbot import chatbot_service
from app.services.chat_memory import ChatMemoryService
from app.services.session_service import SessionService
from app.services.message_service import MessageService
from app.models.chat_session import ChatSession


class ChatService:
    SESSION_COOKIE_NAME = "chat_session_uuid"

    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.redis = redis
        self.session_service = SessionService(db)
        self.memory_service = ChatMemoryService(redis)
        self.message_service = MessageService(db)

    async def resolve_session(
        self,
        request: Request,
        response: Response,
        session_uuid_input: str | None = None,
    ) -> tuple[ChatSession, str]:
        session_uuid = (
            session_uuid_input
            or request.cookies.get(self.SESSION_COOKIE_NAME)
            or request.headers.get("X-Session-UUID")
        )

        session = None
        if session_uuid:
            session = await self.session_service.get_session_by_uuid(session_uuid)

        if not session:
            session_uuid = str(uuid.uuid4())
            user_id = getattr(request.state, "user_id", None)
            session = await self.session_service.create_session(
                session_uuid=session_uuid,
                user_id=user_id,
                ip_address=request.client.host,
                user_agent=request.headers.get("User-Agent"),
                platform=request.headers.get("X-Platform"),
            )

            response.set_cookie(
                key=self.SESSION_COOKIE_NAME,
                value=session_uuid,
                httponly=True,
                samesite="lax",
                secure=False,
                max_age=3600 * 24 * 7,
                path="/",
            )
        else:
            await self.session_service.update_session_last_activity(session_uuid)

        return session, session_uuid

    async def chat(
        self, session: ChatSession, session_uuid: str, user_message: str
    ) -> Dict[str, Any]:
        # 1. Save user message to DB & Redis
        await self.message_service.create_message(session.id, "user", user_message)
        await self.memory_service.add_message(session_uuid, "user", user_message)

        # 2. Get history for bot
        history = await self.memory_service.get_messages(session_uuid)

        # 3. Get bot response
        start_time = time.time()
        bot_response = await chatbot_service.get_answer(user_message, history)
        duration_ms = int((time.time() - start_time) * 1000)

        # 4. Save bot response to DB & Redis
        await self.message_service.create_message(
            session.id, "assistant", bot_response, response_time_ms=duration_ms
        )
        await self.memory_service.add_message(session_uuid, "assistant", bot_response)

        return {
            "response": bot_response,
            "context_length": len(history) + 1,
            "session_uuid": session_uuid,
        }

    async def get_history(self, session: ChatSession) -> List[Dict[str, Any]]:
        messages = await self.message_service.get_messages_by_session(session.id)
        return [
            {"role": m.role, "content": m.content, "created_at": m.created_at}
            for m in messages
        ]

    async def clear_chat(self, session_uuid: str):
        await self.memory_service.clear_memory(session_uuid)

    async def get_complete_conversation_from_session(
        self, session_id: int
    ) -> List[Dict[str, Any]]:
        try:
            all_messages = await self.message_service.get_messages_by_session(
                session_id
            )
            return [
                {
                    "id": m.id,
                    "role": m.role,
                    "content": m.content,
                    "created_at": m.created_at.isoformat() if m.created_at else None,
                    "response_time_ms": m.response_time_ms,
                    "tokens_used": m.tokens_used,
                }
                for m in all_messages
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
