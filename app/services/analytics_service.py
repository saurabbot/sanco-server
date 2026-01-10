from typing import Any, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from app.models.analytics_event import AnalyticsEvent
from app.models.chat_session import ChatSession
from app.models.message import Message
from app.models.lead import Lead
from datetime import datetime, timedelta

class AnalyticsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(self, session_id: int, event_type: str, meta_data: Dict[str, Any] | None = None) -> AnalyticsEvent:
        event = AnalyticsEvent(
            session_id=session_id,
            event_type=event_type,
            meta_data=meta_data
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_overview_stats(self) -> Dict[str, Any]:
        total_sessions = await self.db.scalar(select(func.count(ChatSession.id)))
        total_messages = await self.db.scalar(select(func.count(Message.id)))
        total_leads = await self.db.scalar(select(func.count(Lead.id)))
        
        # Calculate conversion rate (leads / sessions)
        conversion_rate = (total_leads / total_sessions * 100) if total_sessions > 0 else 0
        
        # Average response time
        avg_response_time = await self.db.scalar(
            select(func.avg(Message.response_time_ms))
            .where(Message.role == "assistant")
        )

        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "total_leads": total_leads,
            "conversion_rate": round(conversion_rate, 2),
            "avg_response_time_ms": round(avg_response_time or 0, 2)
        }

    async def get_daily_activity(self, days: int = 7) -> List[Dict[str, Any]]:
        since_date = datetime.now() - timedelta(days=days)
        
        # Group sessions by day
        query = (
            select(
                func.date(ChatSession.created_at).label("date"),
                func.count(ChatSession.id).label("sessions"),
                func.count(Lead.id).label("leads")
            )
            .outerjoin(Lead, ChatSession.id == Lead.session_id)
            .where(ChatSession.created_at >= since_date)
            .group_by(func.date(ChatSession.created_at))
            .order_by(func.date(ChatSession.created_at))
        )
        
        result = await self.db.execute(query)
        return [
            {"date": str(row.date), "sessions": row.sessions, "leads": row.leads} 
            for row in result.all()
        ]

    async def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        query = (
            select(
                ChatSession,
                func.count(Message.id).label("message_count")
            )
            .outerjoin(Message, ChatSession.id == Message.session_id)
            .group_by(ChatSession.id)
            .order_by(desc(ChatSession.created_at))
            .limit(limit)
        )
        result = await self.db.execute(query)
        
        return [
            {
                "id": s.id,
                "session_uuid": s.session_uuid,
                "created_at": s.created_at,
                "ip_address": s.ip_address,
                "platform": s.platform,
                "message_count": msg_count,
                "session_type": s.session_type
            }
            for s, msg_count in result.all()
        ]

    async def get_leads(self, skip: int = 0, limit: int = 50) -> List[Lead]:
        query = (
            select(Lead)
            .order_by(desc(Lead.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_session_detail(self, session_id: int) -> Dict[str, Any]:
        query = select(ChatSession).where(ChatSession.id == session_id)
        result = await self.db.execute(query)
        session = result.scalar_one_or_none()
        
        if not session:
            return None
            
        # Manually load messages to avoid lazy-loading issues
        msg_query = select(Message).where(Message.session_id == session_id).order_by(Message.created_at.asc())
        msg_result = await self.db.execute(msg_query)
        messages = msg_result.scalars().all()
        
        return {
            "session": session,
            "messages": messages
        }