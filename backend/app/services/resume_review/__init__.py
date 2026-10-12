"""
Resume Review & ATS Scoring Microservice Module.
Isolated service for PDF extraction, deterministic parsing, keyword matching,
formatting evaluation, score assignment, database logging, and applicant ranking.
"""

from app.services.resume_review.api import router
from app.services.resume_review.service import (
    analyze_resume,
    get_all_candidate_applicants,
    rank_applicants
)
from app.services.resume_review.parser import parse_complete_resume, extract_text_and_layout
from app.models.resume import ResumeReport, CandidateApplicant
from app.services.resume_review.schemas import (
    ResumeAnalysisReport,
    ResumeScoreCategory,
    ResumeImprovement,
    ResumeSkillGroup,
    ParsedResumeData,
    ParsedContactInfo,
    ParsedEducationEntry,
    ParsedWorkExperienceEntry,
    CandidateApplicantSchema,
    ApplicantRankingResponse
)

__all__ = [
    "router",
    "analyze_resume",
    "get_all_candidate_applicants",
    "rank_applicants",
    "parse_complete_resume",
    "extract_text_and_layout",
    "ResumeReport",
    "CandidateApplicant",
    "ResumeAnalysisReport",
    "ResumeScoreCategory",
    "ResumeImprovement",
    "ResumeSkillGroup",
    "ParsedResumeData",
    "ParsedContactInfo",
    "ParsedEducationEntry",
    "ParsedWorkExperienceEntry",
    "CandidateApplicantSchema",
    "ApplicantRankingResponse"
]
