import json
from typing import List, Dict
from redis.asyncio import Redis

class ChatMemoryService:
    def __init__(self, redis: Redis, window_size: int = 10, ttl: int = 3600):
        self.redis = redis
        self.window_size = window_size
        self.ttl = ttl

    def _get_key(self, identifier: str) -> str:
        return f"chat_mem:{identifier}"

    async def add_message(self, identifier: str, role: str, content: str):
        key = self._get_key(identifier)
        message = json.dumps({"role": role, "content": content})
        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.rpush(key, message)
            pipe.ltrim(key, -self.window_size, -1)
            pipe.expire(key, self.ttl)
            await pipe.execute()

    async def get_messages(self, identifier: str) -> List[Dict[str, str]]:
        key = self._get_key(identifier)
        messages = await self.redis.lrange(key, 0, -1)
        return [json.loads(m) for m in messages]

    async def clear_memory(self, identifier: str):
        await self.redis.delete(self._get_key(identifier))
