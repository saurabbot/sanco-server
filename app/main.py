from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
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
