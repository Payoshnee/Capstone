from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class ResumeReport(Base):
    __tablename__ = "resume_reports"
    
    # Linked to shared users/profiles
    user_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    profile_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    target_role: Mapped[str | None] = mapped_column(String, nullable=True)
    overall_score: Mapped[int | None] = mapped_column(nullable=True)
    grade: Mapped[str | None] = mapped_column(String, nullable=True)
    report_data: Mapped[dict] = mapped_column(JSON)
