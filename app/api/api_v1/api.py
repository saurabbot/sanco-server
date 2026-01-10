from fastapi import APIRouter
from app.api.api_v1.endpoints import users, chat, analytics, auth, livekit, transcriptions

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(livekit.router, prefix="/livekit", tags=["livekit"])
api_router.include_router(transcriptions.router, prefix="/transcriptions", tags=["transcriptions"])
