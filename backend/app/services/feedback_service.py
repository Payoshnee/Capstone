from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate

class FeedbackService:

    @staticmethod
    async def create_feedback(
        db: AsyncSession,
        feedback_in: FeedbackCreate
    ) -> Feedback:

        feedback = Feedback(
            session_id=feedback_in.session_id,
            communication_score=feedback_in.communication_score,
            technical_score=feedback_in.technical_score,
            problem_solving_score=feedback_in.problem_solving_score,
            comments=feedback_in.comments,
            authored_by=feedback_in.authored_by,
        )

        db.add(feedback)
        await db.commit()
        await db.refresh(feedback)
        return feedback

    @staticmethod
    async def get_feedback(
        db: AsyncSession,
        session_id: str
    ) -> Optional[Feedback]:
        result = await db.execute(
            select(Feedback).where(
                Feedback.session_id == session_id
            )
        )
        return result.scalar_one_or_none()

feedback_service = FeedbackService()
