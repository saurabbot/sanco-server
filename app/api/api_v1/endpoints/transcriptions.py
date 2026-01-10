from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.db.session import get_db
from app.services.transcription_service import TranscriptionService

router = APIRouter()

@router.get("/{session_id}", response_model=List[schemas.TranscriptionResponse])
async def get_transcription_by_session(
    session_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    service = TranscriptionService(db)
    transcriptions = await service.get_transcriptions_by_session(session_id)
    print(transcriptions)
    if not transcriptions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No transcriptions found for session {session_id}"
        )
    return transcriptions

@router.post("/{transcription_id}/summarize", response_model=schemas.TranscriptionResponse)
async def summarize_transcription(
    transcription_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    service = TranscriptionService(db)
    transcription = await service.generate_and_store_summary(transcription_id)
    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transcription {transcription_id} not found"
        )
    return transcription
