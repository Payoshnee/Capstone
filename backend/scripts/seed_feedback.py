import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from app.core.config import settings
from app.models.feedback import Feedback
import uuid

async def seed_feedback():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session_maker() as session:
        # Check if dummy feedback exists
        res = await session.execute(text("SELECT count(*) FROM feedback WHERE session_id = 'demo-session-002'"))
        if res.scalar() == 0:
            fb = Feedback(
                id=str(uuid.uuid4()),
                session_id="demo-session-002",
                communication_score=85,
                technical_score=92,
                problem_solving_score=88,
                overall_score=88,
                comments="Strong system design fundamentals. Could improve on handling distributed locking edge cases.",
                authored_by="Alex Rivera"
            )
            session.add(fb)
            await session.commit()
            print("Added dummy feedback for session: demo-session-002")
        else:
            print("Dummy feedback already exists.")

if __name__ == "__main__":
    asyncio.run(seed_feedback())
