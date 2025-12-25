import json
from typing import List, Dict
from redis.asyncio import Redis

class ChatMemoryService:
    def __init__(self, redis: Redis, window_size: int = 10, ttl: int = 3600):
        """
        :param window_size: Number of messages to keep in the hot memory context.
        :param ttl: Time in seconds before the conversation is forgotten (1 hour default).
        """
        self.redis = redis
        self.window_size = window_size
        self.ttl = ttl

    def _get_key(self, identifier: str) -> str:
        return f"chat_mem:{identifier}"

    async def add_message(self, identifier: str, role: str, content: str):
        """Adds a message to the rolling window for a specific user/IP."""
        key = self._get_key(identifier)
        message = json.dumps({"role": role, "content": content})
        
        # Use a transaction-like pipeline for atomic operations
        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.rpush(key, message)      # Append new message
            pipe.ltrim(key, -self.window_size, -1)  # Keep only the last N
            pipe.expire(key, self.ttl)    # Refresh TTL
            await pipe.execute()

    async def get_messages(self, identifier: str) -> List[Dict[str, str]]:
        """Retrieves the context window for the LLM prompt."""
        key = self._get_key(identifier)
        messages = await self.redis.lrange(key, 0, -1)
        return [json.loads(m) for m in messages]

    async def clear_memory(self, identifier: str):
        """Manually clear context for a specific user."""
        await self.redis.delete(self._get_key(identifier))
