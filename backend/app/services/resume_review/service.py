import io
from pypdf import PdfReader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.resume_review.schemas import ResumeAnalysisReport
from app.services.ai_service import ai_service
from app.services.resume_review.models import ResumeReport
from app.models.user import Profile

async def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

async def analyze_resume(
    file_bytes: bytes,
    target_role: str | None = None,
    user_id: str | None = None,
    db: AsyncSession | None = None
) -> ResumeAnalysisReport:
    # 1. Extract text from PDF
    text = await extract_text_from_pdf(file_bytes)
    
    # 2. Score with AI Service (Gemini -> Groq -> Mock Fallback)
    result_dict = ai_service.analyze_resume(text, target_role)
    report = ResumeAnalysisReport(**result_dict)
    
    # 3. Persist to isolated resume_reports table and connect with Profile if DB available
    if db:
        try:
            profile_id = None
            if user_id:
                profile_res = await db.execute(select(Profile).where(Profile.user_id == user_id))
                profile = profile_res.scalar_one_or_none()
                if profile:
                    profile_id = profile.id
            
            db_report = ResumeReport(
                user_id=user_id,
                profile_id=profile_id,
                target_role=target_role,
                overall_score=report.overall_score,
                grade=report.grade,
                report_data=report.model_dump()
            )
            db.add(db_report)
            await db.commit()
        except Exception as e:
            await db.rollback()
            # Log warning without blocking the candidate from getting their report
            print(f"Warning: could not persist resume report to DB: {e}")
            
    return report
