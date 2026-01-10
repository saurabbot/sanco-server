from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.db.session import get_db
from app.core.config import settings
from app.services.livekit_service import livekit_service
# Assuming you have a dependency to get the current user
# from app.api.deps import get_current_user 

router = APIRouter()

@router.post("/token", response_model=schemas.livekit.LiveKitTokenResponse)
async def get_livekit_token(
    request_in: schemas.livekit.LiveKitTokenRequest,
    # current_user: models.User = Depends(get_current_user)
) -> Any:
    if not settings.LIVEKIT_API_KEY or not settings.LIVEKIT_API_SECRET:
        raise HTTPException(status_code=500, detail="LiveKit configuration missing")

    # Create room if it doesn't exist
    await livekit_service.create_room(request_in.roomName)

    # identity = request_in.participantIdentity or str(current_user.id)
    # name = request_in.participantName or current_user.full_name
    identity = request_in.participantIdentity or "guest"
    name = request_in.participantName or "Guest"

    token = await livekit_service.get_token(
        room_name=request_in.roomName,
        identity=identity,
        name=name
    )

    return {
        "token": token,
        "serverUrl": settings.LIVEKIT_URL
    }

@router.post("/dispatch")
async def dispatch_livekit_agent(
    request_in: schemas.livekit.LiveKitAgentRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    if not settings.LIVEKIT_API_KEY or not settings.LIVEKIT_API_SECRET:
        raise HTTPException(status_code=500, detail="LiveKit configuration missing")

    agent_name = settings.LIVEKIT_AGENT_NAME
    
    # Metadata construction similar to Node code
    agent_meta_data = {
        "room": request_in.room,
        "url": request_in.url,
        "content_id": request_in.id,
        # Add user placeholders for future auth integration
        "user_id": None,
        "user_name": "Guest"
    }

    await livekit_service.dispatch_agent(
        room_name=request_in.room,
        agent_name=agent_name,
        metadata=agent_meta_data
    )

    return {"success": True}

