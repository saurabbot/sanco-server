from sqlalchemy import select
from app.models.chat_session import ChatSession
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


class SessionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(
        self,
        session_uuid: str,
        user_id: int | None,
        ip_address: str,
        user_agent: str | None,
        platform: str | None,
    ):
        session = ChatSession(
            session_uuid=session_uuid,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            platform=platform,
        )
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_session_by_uuid(self, session_uuid: str):
        result = await self.db.execute(
            select(ChatSession).where(ChatSession.session_uuid == session_uuid)
        )
        return result.scalar_one_or_none()

    async def update_session_last_activity(self, session_uuid: str):
        session = await self.get_session_by_uuid(session_uuid)
        if session:
            session.last_activity_at = datetime.now()
            await self.db.commit()
        return session

    async def delete_session(self, session_uuid: str):
        session = await self.get_session_by_uuid(session_uuid)
        await self.db.delete(session)
        await self.db.commit()
        return session
