from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TranscriptionBase(BaseModel):
    session_id: int
    transcription: str
    start_time: datetime
    end_time: datetime
    transcription_summary: Optional[str] = None


class TranscriptionResponse(TranscriptionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
