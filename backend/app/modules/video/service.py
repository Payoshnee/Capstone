from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.modules.video.models import VideoSession


class VideoService:

    @staticmethod
    async def create_session(
        db: AsyncSession,
        user_id: str
    ) -> VideoSession:

        session_id = str(uuid4())
        room_name = f"capstone-{session_id}"

        session = VideoSession(
            id=session_id,
            room_name=room_name,
            user_id=user_id,
            status="waiting",
            created_at=datetime.now(timezone.utc)
        )

        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def get_session(
        db: AsyncSession,
        session_id: str
    ) -> VideoSession | None:
        result = await db.execute(select(VideoSession).where(VideoSession.id == session_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def join_session(
        db: AsyncSession,
        session_id: str
    ) -> VideoSession | None:
        session = await VideoService.get_session(db, session_id)
        if not session:
            return None

        if session.status == "waiting":
            session.status = "active"
            await db.commit()
            await db.refresh(session)

        return session

    @staticmethod
    async def end_session(
        db: AsyncSession,
        session_id: str
    ) -> VideoSession | None:
        session = await VideoService.get_session(db, session_id)
        if not session:
            return None

        session.status = "ended"
        session.ended_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(session)

        return session

video_service = VideoService()
