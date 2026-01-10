from typing import Any, Dict, Optional
from pydantic import BaseModel

class LiveKitTokenRequest(BaseModel):
    roomName: str
    roomId: Optional[str] = None
    participantName: Optional[str] = None
    participantIdentity: Optional[str] = None

class LiveKitTokenResponse(BaseModel):
    token: str
    serverUrl: str

class LiveKitAgentRequest(BaseModel):
    room: str
    url: Optional[str] = None
    id: Optional[str] = None # Support both id and url

