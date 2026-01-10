from typing import Any, List
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app import schemas
from app.db.session import get_db
from app.core.redis import get_redis
from app.services.analytics_service import AnalyticsService
from app.services.chat_service import ChatService

router = APIRouter()

# --- Public Endpoints (for Widget) ---

@router.post("/events")
async def create_analytics_event(
    event_in: schemas.analytics.AnalyticsEventCreate,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> Any:
    chat_service = ChatService(db, redis)
    session, session_uuid = await chat_service.resolve_session(
        request, 
        response, 
        event_in.session_uuid
    )
    
    analytics_service = AnalyticsService(db)
    event = await analytics_service.create_event(
        session_id=session.id,
        event_type=event_in.event_type,
        meta_data=event_in.meta_data
    )
    
    return {"status": "success", "event_id": event.id, "session_uuid": session_uuid}


# --- Protected Dashboard Endpoints ---

@router.get("/overview", response_model=schemas.analytics.DashboardOverview)
async def get_dashboard_overview(
    db: AsyncSession = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_overview_stats()


@router.get("/daily-activity", response_model=List[schemas.analytics.DailyActivity])
async def get_daily_activity(
    days: int = 7,
    db: AsyncSession = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_daily_activity(days=days)


@router.get("/recent-sessions", response_model=List[schemas.analytics.SessionSummary])
async def get_recent_sessions(
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_recent_sessions(limit=limit)


@router.get("/leads", response_model=List[schemas.analytics.LeadSummary])
async def get_leads(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    return await analytics_service.get_leads(skip=skip, limit=limit)


@router.get("/sessions/{session_id}", response_model=schemas.analytics.SessionDetail)
async def get_session_detail(
    session_id: int,
    db: AsyncSession = Depends(get_db)
):
    analytics_service = AnalyticsService(db)
    session_data = await analytics_service.get_session_detail(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Map to SessionSummary manually to include message_count
    session = session_data["session"]
    summary = schemas.analytics.SessionSummary(
        id=session.id,
        session_uuid=session.session_uuid,
        created_at=session.created_at,
        ip_address=session.ip_address,
        platform=session.platform,
        message_count=len(session_data["messages"])
    )
    
    return {
        "session": summary,
        "messages": session_data["messages"]
    }
