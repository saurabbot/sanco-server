import openai
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.transcriptions import Transcription
from app.core.config import settings


class TranscriptionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def get_transcriptions_by_session(
        self, session_id: int
    ) -> List[Transcription]:
        query = (
            select(Transcription)
            .where(Transcription.session_id == session_id)
            .order_by(Transcription.start_time)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_transcription(self, transcription_id: int) -> Optional[Transcription]:
        query = select(Transcription).where(Transcription.id == transcription_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def generate_and_store_summary(
        self, transcription_id: int
    ) -> Optional[Transcription]:

        transcription_obj = await self.get_transcription(transcription_id)
        if not transcription_obj:
            return None

        if transcription_obj.transcription_summary:
            return transcription_obj

        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following transcription accurately and concisely.",
                },
                {"role": "user", "content": transcription_obj.transcription},
            ],
        )
        summary = response.choices[0].message.content

        await self.db.execute(
            update(Transcription)
            .where(Transcription.id == transcription_id)
            .values(transcription_summary=summary)
        )
        await self.db.commit()

        await self.db.refresh(transcription_obj)
        return transcription_obj
