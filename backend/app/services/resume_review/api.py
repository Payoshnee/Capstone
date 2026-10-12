from fastapi import APIRouter, UploadFile, File, Form, Depends, Body
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.resume_review.schemas import (
    ResumeAnalysisReport,
    CandidateApplicantSchema,
    ApplicantRankingResponse,
    ApplicantRankingItem,
    RankApplicantsRequest,
    MatchJDRequest,
    JDMatchDetail
)
from app.schemas.common import APIResponse, APIError
from app.services.resume_review.service import (
    analyze_resume,
    get_all_candidate_applicants,
    rank_applicants
)
from app.services.resume_review.matcher import match_resume_against_jd
from app.services.resume_review.keyword_pool import ROLE_PROFILES, PROGRAMMING_LANGUAGES, FRAMEWORKS_AND_LIBRARIES, DATABASES_AND_STORAGE, CLOUD_AND_DEVOPS, CORE_CONCEPTS
from app.core.database import get_db
from app.services.ai_service import ai_service
from app.models.resume import ResumeReport

router = APIRouter()

@router.get("/health")
async def resume_service_health():
    return {"service": "resume_review", "status": "healthy"}

@router.get("/keywords", response_model=APIResponse[Dict[str, Any]])
async def get_ats_keyword_taxonomies():
    """Returns available SDE & Data roles, tracks, and tech taxonomies for ATS matching."""
    roles_summary = [
        {
            "role_key": k,
            "title": v["title"],
            "track": v["track"],
            "core_skills": v["core_skills"],
            "core_languages": v["core_languages"],
            "preferred_tools": v["preferred_tools"]
        }
        for k, v in ROLE_PROFILES.items()
    ]
    taxonomies = {
        "roles": roles_summary,
        "programming_languages": sorted(list(PROGRAMMING_LANGUAGES)),
        "frameworks_and_libraries": sorted(list(FRAMEWORKS_AND_LIBRARIES)),
        "databases_and_storage": sorted(list(DATABASES_AND_STORAGE)),
        "cloud_and_devops": sorted(list(CLOUD_AND_DEVOPS)),
        "core_concepts": sorted(list(CORE_CONCEPTS))
    }
    return APIResponse(data=taxonomies)

@router.post("/analyze", response_model=APIResponse[ResumeAnalysisReport])
async def upload_resume(
    file: UploadFile = File(...),
    target_role: str | None = Form(None),
    job_description: str | None = Form(None),
    candidate_name: str | None = Form(None),
    candidate_email: str | None = Form(None),
    user_id: str | None = Form(None),
    db: AsyncSession | None = Depends(get_db)
):
    """
    Primary ATS Upload & Scoring Endpoint:
    - Accepts PDF resume
    - Extracts structured contact details, work history, education, skills
    - Matches keywords against target role and optional Job Description
    - Evaluates section completeness & layout readability
    - Calculates ATS composite score (0-100) & letter grade
    - Logs applicant into candidate database
    """
    try:
        content = await file.read()
        if not file.filename or not file.filename.lower().endswith('.pdf'):
            return APIResponse(error=APIError(message="Only PDF files are supported"))
            
        report = await analyze_resume(
            file_bytes=content,
            target_role=target_role,
            job_description=job_description,
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            user_id=user_id,
            db=db
        )
        return APIResponse(data=report)
    except Exception as e:
        return APIResponse(error=APIError(message=str(e)))

@router.get("/candidates", response_model=APIResponse[List[CandidateApplicantSchema]])
async def list_candidate_applicants(db: AsyncSession | None = Depends(get_db)):
    """Retrieve all applicants logged into the candidate database."""
    try:
        applicants = await get_all_candidate_applicants(db)
        schemas = [CandidateApplicantSchema(**a) for a in applicants]
        return APIResponse(data=schemas)
    except Exception as e:
        return APIResponse(error=APIError(message=str(e)))

@router.post("/rank", response_model=APIResponse[ApplicantRankingResponse])
async def rank_candidates(
    req: RankApplicantsRequest = Body(default_factory=RankApplicantsRequest),
    db: AsyncSession | None = Depends(get_db)
):
    """
    Candidate Ranking:
    Ranks applicants from highest to lowest match score for a given target role or Job Description.
    """
    try:
        ranked = await rank_applicants(
            target_role=req.target_role,
            job_description=req.job_description,
            db=db
        )
        items = [ApplicantRankingItem(**r) for r in ranked]
        target_display = req.job_description[:60] + "..." if req.job_description else (req.target_role or "All SDE & Data Roles")
        response = ApplicantRankingResponse(
            target_role_or_jd=target_display,
            total_applicants=len(items),
            ranked_applicants=items
        )
        return APIResponse(data=response)
    except Exception as e:
        return APIResponse(error=APIError(message=str(e)))

@router.post("/match-jd", response_model=APIResponse[JDMatchDetail])
async def match_against_jd(
    req: MatchJDRequest,
    db: AsyncSession | None = Depends(get_db)
):
    """Compare raw resume text or a registered applicant's resume against a custom Job Description."""
    try:
        resume_text = req.resume_text or ""
        if not resume_text and req.applicant_id:
            all_apps = await get_all_candidate_applicants(db)
            matched_app = next((a for a in all_apps if a["id"] == req.applicant_id), None)
            if matched_app and matched_app.get("raw_text"):
                resume_text = matched_app["raw_text"]
                
        if not resume_text:
            return APIResponse(error=APIError(message="No resume text or valid applicant_id provided"))
            
        res = match_resume_against_jd(
            resume_text=resume_text,
            parsed_skills={},
            job_description=req.job_description
        )
        return APIResponse(data=JDMatchDetail(**res))
    except Exception as e:
        return APIResponse(error=APIError(message=str(e)))

@router.get("/reports/{report_id}", response_model=APIResponse[ResumeAnalysisReport])
async def get_report(report_id: str, db: AsyncSession | None = Depends(get_db)):
    """Fetch report by ID from database or sample mock."""
    if not db:
        mock_data = ai_service.get_mock_fallback("Software Engineer")
        return APIResponse(data=ResumeAnalysisReport(**mock_data))
    try:
        report = await db.get(ResumeReport, report_id)
        if not report:
            return APIResponse(error=APIError(message="Report not found"))
        return APIResponse(data=ResumeAnalysisReport(**report.report_data))
    except Exception as e:
        return APIResponse(error=APIError(message=str(e)))

@router.get("/sample", response_model=APIResponse[ResumeAnalysisReport])
async def get_sample_report():
    mock_data = ai_service.get_mock_fallback("Software Engineer")
    return APIResponse(data=ResumeAnalysisReport(**mock_data))
