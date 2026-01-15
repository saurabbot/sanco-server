import uuid
import time
from typing import Dict, Any, List
from fastapi import Request, Response, HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lead import Lead
from app import schemas


class LeadService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_lead(self, session_id: int, lead_data: schemas.Lead) -> Lead:
        lead = Lead(
            session_id=session_id,
            name=lead_data.name,
            email=lead_data.email,
            phone=lead_data.phone,
            ip_address=ip_address,
        )
        self.db.add(lead)
        await self.db.commit()
        await self.db.refresh(lead)
        return lead
