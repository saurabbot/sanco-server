from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_uuid: Optional[str] = None
    sessionuuid: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    context_length: int
    session_uuid: str
