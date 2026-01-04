from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ChatFeedback(Base):
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("message.id"), nullable=False, unique=True)
    rating = Column(Integer)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    message = relationship("Message", back_populates="feedback")

