import redis.asyncio as redis
from app.core.config import settings

# Create a connection pool for scalability
redis_pool = redis.ConnectionPool.from_url(
    settings.REDIS_URL, 
    max_connections=100, 
    decode_responses=True
)

def get_redis():
    """Dependency for FastAPI to get a Redis connection."""
    return redis.Redis(connection_pool=redis_pool)
