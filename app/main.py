from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db import base  # noqa: F401

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
# We must be extremely explicit when allow_credentials=True
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Add origins from settings if they aren't already there
for origin in settings.BACKEND_CORS_ORIGINS:
    origin_str = str(origin).rstrip("/")
    if origin_str not in origins:
        origins.append(origin_str)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    print(f"🚀 {settings.PROJECT_NAME} is starting up...")
    # Strip asyncpg for Beekeeper compatibility
    db_url = str(settings.SQLALCHEMY_DATABASE_URI).replace("+asyncpg", "")
    print(f"💾 Database URL (Beekeeper): {db_url}")

app.include_router(api_router, prefix=settings.API_V1_STR)
