from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.schemas.common import APIResponse, APIError
from app.schemas.feedback import FeedbackCreate, FeedbackResponse, FeedbackReport
from app.services.feedback_service import feedback_service


router = APIRouter()


def feedback_to_response(feedback) -> FeedbackResponse:
    return FeedbackResponse(
        id=feedback.id,
        session_id=feedback.session_id,
        communication_score=feedback.communication_score,
        technical_score=feedback.technical_score,
        problem_solving_score=feedback.problem_solving_score,
        comments=feedback.comments,
        authored_by=feedback.authored_by,
    )


@router.post("", response_model=APIResponse[FeedbackResponse])
async def create_feedback(
    feedback_in: FeedbackCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        feedback = await feedback_service.create_feedback(db, feedback_in)

        return APIResponse(
            data=feedback_to_response(feedback)
        )

    except Exception as e:
        return APIResponse(
            error=APIError(message=str(e))
        )


@router.get(
    "/{session_id}",
    response_model=APIResponse[FeedbackReport]
)
async def get_feedback(
    session_id: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        feedback = await feedback_service.get_feedback(db, session_id)

        if not feedback:
            return APIResponse(
                error=APIError(message="Feedback not found for this session")
            )

        # Support both 1-5 and 0-100 score scales seamlessly
        def norm(s: int | float) -> float:
            return round(s / 20.0, 1) if s > 5 else float(s)

        comm_5 = norm(feedback.communication_score)
        tech_5 = norm(feedback.technical_score)
        ps_5 = norm(feedback.problem_solving_score)

        overall_score = round((comm_5 + tech_5 + ps_5) / 3, 1)

        strengths = []
        areas_for_improvement = []

        if comm_5 >= 4.0:
            strengths.append("Clear and effective communication.")
        elif comm_5 <= 2.5:
            areas_for_improvement.append(
                "Improve clarity and confidence while communicating."
            )

        if tech_5 >= 4.0:
            strengths.append("Strong technical understanding.")
        elif tech_5 <= 2.5:
            areas_for_improvement.append(
                "Strengthen technical concepts and accuracy."
            )

        if ps_5 >= 4.0:
            strengths.append(
                "Good logical and problem-solving approach."
            )
        elif ps_5 <= 2.5:
            areas_for_improvement.append(
                "Practice breaking problems into clear, logical steps."
            )

        if not strengths:
            strengths.append(
                "Shows solid baseline competency across evaluated categories."
            )

        if not areas_for_improvement:
            areas_for_improvement.append(
                "Continue practicing to maintain consistent interview performance under pressure."
            )

        recommendation = (
            "Keep practicing mock interviews and focus on giving structured, "
            "confident answers while strengthening areas with lower scores."
        )

        return APIResponse(
            data=FeedbackReport(
                id=feedback.id,
                session_id=feedback.session_id,
                communication_score=round(comm_5),
                technical_score=round(tech_5),
                problem_solving_score=round(ps_5),
                comments=feedback.comments,
                authored_by=feedback.authored_by,
                overall_score=overall_score,
                strengths=strengths,
                areas_for_improvement=areas_for_improvement,
                recommendation=recommendation,
            )
        )

    except Exception as e:
        return APIResponse(error=APIError(message=str(e)))