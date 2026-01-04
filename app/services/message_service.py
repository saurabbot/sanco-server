from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.message import Message
from typing import List

class MessageService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_message(
        self, 
        session_id: int, 
        role: str, 
        content: str, 
        response_time_ms: int | None = None,
        tokens_used: int | None = None
    ) -> Message:
        message = Message(
            session_id=session_id,
            role=role,
            content=content,
            response_time_ms=response_time_ms,
            tokens_used=tokens_used
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_messages_by_session(self, session_id: int) -> List[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at.asc())
        )
        return result.scalars().all()

