from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class AnalyticsEvent(Base):
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chatsession.id"), nullable=False)
    event_type = Column(String, index=True, nullable=False)
    meta_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    session = relationship("ChatSession", back_populates="events")

