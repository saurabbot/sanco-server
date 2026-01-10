from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.chat_session import SessionType
class AnalyticsEventCreate(BaseModel):
    event_type: str
    meta_data: Optional[Dict[str, Any]] = None
    session_uuid: Optional[str] = None

class DashboardOverview(BaseModel):
    total_sessions: int
    total_messages: int
    total_leads: int
    conversion_rate: float
    avg_response_time_ms: float

class DailyActivity(BaseModel):
    date: str
    sessions: int
    leads: int

class SessionSummary(BaseModel):
    id: int
    session_uuid: str
    created_at: datetime
    ip_address: Optional[str]
    platform: Optional[str]
    message_count: int
    session_type: SessionType

class LeadSummary(BaseModel):
    id: int
    name: Optional[str]
    email: str
    phone: Optional[str]
    ip_address: Optional[str]
    created_at: datetime
    session_id: Optional[int]

class MessageDetail(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    response_time_ms: Optional[int]

class SessionDetail(BaseModel):
    session: SessionSummary
    messages: List[MessageDetail]