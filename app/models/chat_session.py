from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ChatSession(Base):
    id = Column(Integer, primary_key=True, index=True)
    session_uuid = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    ip_address = Column(String, index=True)
    user_agent = Column(String, nullable=True)
    platform = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    last_activity_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="session")
    events = relationship("AnalyticsEvent", back_populates="session", cascade="all, delete-orphan")

