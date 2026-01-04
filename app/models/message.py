from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chatsession.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(String, nullable=False)
    tokens_used = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    session = relationship("ChatSession", back_populates="messages")
    feedback = relationship("ChatFeedback", back_populates="message", uselist=False)
    