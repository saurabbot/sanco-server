from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class ServiceMedia(Base):
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    media_type = Column(String, nullable=False)
    media_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    service = relationship("Services", back_populates="media")
