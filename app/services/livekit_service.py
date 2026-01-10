import json
from typing import Optional, List
from livekit import api
from app.core.config import settings

class LiveKitService:
    def __init__(self):
        self.api_key = settings.LIVEKIT_API_KEY
        self.api_secret = settings.LIVEKIT_API_SECRET
        self.url = settings.LIVEKIT_URL

    async def get_token(
        self, 
        room_name: str, 
        identity: str, 
        name: Optional[str] = None
    ) -> str:
        token = api.AccessToken(self.api_key, self.api_secret) \
            .with_identity(identity) \
            .with_name(name or identity) \
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True
            ))
        return token.to_jwt()

    async def create_room(self, room_name: str):
        lk_api = api.LiveKitAPI(self.url, self.api_key, self.api_secret)
        try:
            req = api.CreateRoomRequest()
            req.name = room_name
            req.empty_timeout = 600
            await lk_api.room.create_room(req)
        except Exception as e:
            # LiveKit Python SDK might not throw "already exists" in a way that's easy to catch without specific error types
            # but usually, creating a room that exists is a no-op or returns the existing room.
            pass
        finally:
            await lk_api.aclose()

    async def dispatch_agent(self, room_name: str, agent_name: str, metadata: dict):
        lk_api = api.LiveKitAPI(self.url, self.api_key, self.api_secret)
        try:
            dispatches = await lk_api.agent_dispatch.list_dispatch(room_name)
            
            for d in dispatches:
                if d.agent_name == agent_name:
                    return d

            create_req = api.CreateAgentDispatchRequest()
            create_req.room = room_name
            create_req.agent_name = agent_name
            create_req.metadata = json.dumps(metadata)
            
            return await lk_api.agent_dispatch.create_dispatch(create_req)
        finally:
            await lk_api.aclose()

livekit_service = LiveKitService()

