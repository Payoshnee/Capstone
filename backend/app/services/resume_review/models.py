from sqlalchemy import String, JSON, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class ResumeReport(Base):
    __tablename__ = "resume_reports"
    
    # Linked to shared users/profiles
    user_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    profile_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    target_role: Mapped[str | None] = mapped_column(String, nullable=True)
    overall_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    grade: Mapped[str | None] = mapped_column(String, nullable=True)
    report_data: Mapped[dict] = mapped_column(JSON)

class CandidateApplicant(Base):
    """Database model logging candidates submitted for ATS analysis and applicant ranking."""
    __tablename__ = "candidate_applicants"
    
    resume_report_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    user_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    candidate_name: Mapped[str] = mapped_column(String, index=True, default="Candidate")
    email: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    target_role: Mapped[str] = mapped_column(String, default="sde")
    job_description_snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # ATS Scoring Metrics
    overall_score: Mapped[int] = mapped_column(Integer, default=0)
    grade: Mapped[str] = mapped_column(String, default="B")
    keyword_match_score: Mapped[int] = mapped_column(Integer, default=0)
    formatting_score: Mapped[int] = mapped_column(Integer, default=0)
    skills_match_score: Mapped[int] = mapped_column(Integer, default=0)
    
    # Serialized summaries
    matched_skills: Mapped[list] = mapped_column(JSON, default=list)
    missing_skills: Mapped[list] = mapped_column(JSON, default=list)
    raw_details: Mapped[dict] = mapped_column(JSON, default=dict)
