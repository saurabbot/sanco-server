from fastapi import APIRouter
from app import schemas
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from app.services.lead_service import LeadService

router = APIRouter()


@router.post("/create_lead")
async def create_lead(
    session_id: int, lead: schemas.Lead, db: AsyncSession = Depends(get_db)
):
    try:
        lead_service = LeadService(db)
        lead = await lead_service.create_lead(session_id, lead)
        return lead
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Lead created successfully"}
