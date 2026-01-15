from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Services(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    short_description = Column(String, nullable=True)
    long_description = Column(String, nullable=True)
    price = Column(Integer, nullable=True)

    media = relationship("ServiceMedia", back_populates="service")
