from fastapi import APIRouter
from app.api.api_v1.endpoints import users, chat

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
