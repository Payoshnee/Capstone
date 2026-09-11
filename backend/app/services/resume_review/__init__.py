"""
Resume Review Microservice Module
Isolated service for PDF extraction, ATS analysis, 4-pillar scoring, and bullet optimization.
"""

from app.services.resume_review.api import router
from app.services.resume_review.service import analyze_resume, extract_text_from_pdf
from app.services.resume_review.models import ResumeReport
from app.services.resume_review.schemas import ResumeAnalysisReport, ResumeScoreCategory, ResumeImprovement, ResumeSkillGroup

__all__ = [
    "router",
    "analyze_resume",
    "extract_text_from_pdf",
    "ResumeReport",
    "ResumeAnalysisReport",
    "ResumeScoreCategory",
    "ResumeImprovement",
    "ResumeSkillGroup"
]
