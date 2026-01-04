import asyncio
import asyncpg
from app.core.config import settings


async def get_db():
    pool = await asyncpg.create_pool(
        dsn=settings.ASYNC_DATABASE_URI,
        min_size=1,
        max_size=10,
        max_queries=100000,
        max_inactive_connection_lifetime=300,
    )
    return pool
