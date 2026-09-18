"""
Resume Review & ATS Scoring Orchestration Service.
Coordinates PDF extraction, deterministic parsing, keyword matching,
formatting evaluation, score assignment, database logging, and applicant ranking.
"""
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.services.resume_review.keyword_pool import (
    ROLE_PROFILES,
    resolve_target_role
)
from app.services.resume_review.parser import parse_complete_resume
from app.services.resume_review.matcher import perform_keyword_matching, match_resume_against_jd
from app.services.resume_review.evaluator import evaluate_formatting_and_layout
from app.services.resume_review.models import ResumeReport, CandidateApplicant
from app.services.resume_review.schemas import (
    ResumeAnalysisReport,
    ResumeScoreCategory,
    ResumeSkillGroup,
    ResumeImprovement,
    ParsedResumeData,
    ParsedContactInfo,
    ParsedEducationEntry,
    ParsedWorkExperienceEntry,
    ParsedSkillsBreakdown,
    LayoutMetrics,
    UnifiedKeywordMatch,
    RoleMatchDetail,
    JDMatchDetail,
    FormattingEvaluation,
    SectionCompletenessDetail,
    ImpactEvaluationDetail
)
from app.services.ai_service import ai_service
from app.models.user import Profile

# In-memory applicant registry ensuring 100% demo functionality even without active PostgreSQL
IN_MEMORY_APPLICANTS: Dict[str, Dict[str, Any]] = {}

def calculate_skills_depth_score(skills_breakdown: Dict[str, List[str]]) -> int:
    """Calculate technical depth score (0-100) based on diversity and volume of technical skills."""
    langs = len(skills_breakdown.get("languages", []))
    frameworks = len(skills_breakdown.get("frameworks_and_libraries", []))
    dbs = len(skills_breakdown.get("databases", []))
    cloud = len(skills_breakdown.get("cloud_and_devops", []))
    concepts = len(skills_breakdown.get("concepts_and_methodologies", []))
    
    # 2+ languages = 25 pts, 2+ frameworks = 25 pts, 1+ db = 20 pts, 1+ cloud = 15 pts, 2+ concepts = 15 pts
    score = 0
    score += min(25, langs * 12)
    score += min(25, frameworks * 12)
    score += min(20, dbs * 10)
    score += min(15, cloud * 15)
    score += min(15, concepts * 7)
    
    return min(100, max(10, score))

def assign_grade(score: int) -> str:
    """Assign letter grade based on ATS score."""
    if score >= 93:
        return "A+"
    elif score >= 88:
        return "A"
    elif score >= 83:
        return "A-"
    elif score >= 78:
        return "B+"
    elif score >= 72:
        return "B"
    elif score >= 67:
        return "B-"
    elif score >= 60:
        return "C+"
    elif score >= 50:
        return "C"
    else:
        return "D"

async def analyze_resume(
    file_bytes: bytes,
    target_role: str | None = None,
    job_description: str | None = None,
    candidate_name: str | None = None,
    candidate_email: str | None = None,
    user_id: str | None = None,
    db: AsyncSession | None = None
) -> ResumeAnalysisReport:
    """
    Complete ATS processing pipeline:
    1. Text & Layout Extraction
    2. Heuristic Parsing (Contact, Education, Work History, Skills)
    3. Keyword Matching against JD and SDE/Data role pool
    4. Formatting & Structure Evaluation
    5. Score Assignment & Grade Calculation
    6. Candidate Database Logging
    """
    # 1. Parse resume text and structural elements
    parsed = parse_complete_resume(file_bytes)
    
    # Override contact details if explicitly provided
    if candidate_name and candidate_name.strip():
        parsed["contact"]["name"] = candidate_name.strip()
    if candidate_email and candidate_email.strip():
        parsed["contact"]["email"] = candidate_email.strip()
        
    resolved_role_key = resolve_target_role(target_role)
    role_info = ROLE_PROFILES.get(resolved_role_key, ROLE_PROFILES["sde"])
    
    # 2. Keyword Matching
    keyword_match_res = perform_keyword_matching(
        resume_text=parsed["layout"]["full_text"],
        parsed_skills=parsed["skills"],
        target_role=resolved_role_key,
        job_description=job_description
    )
    
    # 3. Formatting & Readability Evaluation
    formatting_eval_res = evaluate_formatting_and_layout(
        layout=parsed["layout"],
        contact=parsed["contact"],
        sections=parsed["sections"],
        extracted_skills=parsed["skills"]
    )
    
    # 4. Score Assignment
    keyword_score = keyword_match_res["keyword_score"]
    skills_score = calculate_skills_depth_score(parsed["skills"])
    formatting_score = formatting_eval_res["formatting_score"]
    metrics_score = formatting_eval_res["impact_evaluation"]["quantified_metrics_score"]
    completeness_score = formatting_eval_res["section_completeness"]["completeness_score"]
    
    # Composite formula: Keyword Match 35%, Skills Depth 25%, Formatting/Readability 20%, Impact/Metrics 20%
    overall_score = int(round(
        (keyword_score * 0.35)
        + (skills_score * 0.25)
        + (formatting_score * 0.20)
        + (metrics_score * 0.20)
    ))
    overall_score = min(100, max(15, overall_score))
    grade = assign_grade(overall_score)
    
    # 5. Category Scores
    category_scores = [
        ResumeScoreCategory(
            category_name="Impact & Metrics",
            score=metrics_score,
            weight=0.25,
            feedback_text=f"{formatting_eval_res['impact_evaluation']['bullets_with_metrics']} of {formatting_eval_res['impact_evaluation']['total_bullets_analyzed']} bullets contain quantifiable figures or percentages."
        ),
        ResumeScoreCategory(
            category_name="Technical Depth",
            score=skills_score,
            weight=0.25,
            feedback_text=f"Detected {len(parsed['skills']['languages'])} languages, {len(parsed['skills']['frameworks_and_libraries'])} frameworks, and {len(parsed['skills']['databases'])} databases."
        ),
        ResumeScoreCategory(
            category_name="Keyword & Role Match",
            score=keyword_score,
            weight=0.25,
            feedback_text=(
                f"Matched {keyword_match_res['jd_match']['matched_count']}/{keyword_match_res['jd_match']['total_jd_keywords']} JD keywords ({keyword_match_res['jd_match']['match_percentage']}%)."
                if keyword_match_res.get("jd_match")
                else f"Matched {len(keyword_match_res['role_match']['matched_core_skills'])} core skills for {role_info['title']}."
            )
        ),
        ResumeScoreCategory(
            category_name="Structure & ATS Readability",
            score=completeness_score,
            weight=0.25,
            feedback_text=f"Section completeness is {completeness_score}%. {len(formatting_eval_res['warnings'])} formatting warning(s) flagged."
        )
    ]
    
    # 6. Group skills for frontend display
    skills_groups = [
        ResumeSkillGroup(category="Languages", skills=parsed["skills"]["languages"]),
        ResumeSkillGroup(category="Frameworks & Libraries", skills=parsed["skills"]["frameworks_and_libraries"]),
        ResumeSkillGroup(category="Databases & Storage", skills=parsed["skills"]["databases"]),
        ResumeSkillGroup(category="Cloud & DevOps", skills=parsed["skills"]["cloud_and_devops"]),
        ResumeSkillGroup(category="Concepts & Methodologies", skills=parsed["skills"]["concepts_and_methodologies"]),
    ]
    
    # 7. Strengths, Weaknesses & Improvements
    strengths = []
    if len(parsed["skills"]["languages"]) >= 2:
        strengths.append(f"Strong polyglot foundation with proficiency in {', '.join(parsed['skills']['languages'][:3])}.")
    if metrics_score >= 50:
        strengths.append(f"Effective use of quantifiable metrics ({metrics_score}% of bullets have measurable impact).")
    if completeness_score >= 80:
        strengths.append("Well-structured document with all standard ATS sections present.")
    if keyword_score >= 70:
        strengths.append(f"High technical keyword alignment with the target role ({role_info['title']}).")
    if not strengths:
        strengths.append("Clean baseline structure suitable for automated parser extraction.")
        
    weaknesses = []
    if formatting_eval_res["warnings"]:
        weaknesses.extend(formatting_eval_res["warnings"][:3])
    if keyword_match_res["role_match"]["missing_core_skills"]:
        weaknesses.append(f"Missing core technical keywords: {', '.join(keyword_match_res['role_match']['missing_core_skills'][:3])}.")
    if not weaknesses:
        weaknesses.append("Consider tightening bullet point density and including more business impact numbers.")
        
    # Bullet Improvements
    improvements = []
    sample_bullets = parsed["layout"].get("bullet_lines", [])
    if sample_bullets:
        target_bullet = sample_bullets[0]
        cleaned_b = target_bullet.lstrip("•-*▪–— ").strip()
        improvements.append(ResumeImprovement(
            section="Experience",
            issue="Lacks quantifiable outcome and strong action verb",
            before_text=cleaned_b,
            suggested_text=f"Architected and optimized {cleaned_b}, cutting processing latency by 35% and supporting 10k+ active users.",
            priority="high"
        ))
    else:
        improvements.append(ResumeImprovement(
            section="Experience",
            issue="Paragraph format reduces ATS readability",
            before_text="Worked on developing backend services and database queries.",
            suggested_text="Engineered 12+ RESTful endpoints using FastAPI and PostgreSQL, reducing query latency by 25%.",
            priority="high"
        ))
        
    recommended_topics = keyword_match_res["role_match"].get("recommended_interview_topics", role_info.get("recommended_topics", []))
    
    # 8. Assemble structured models
    parsed_model = ParsedResumeData(
        contact=ParsedContactInfo(**parsed["contact"]),
        education=[ParsedEducationEntry(**e) for e in parsed["education"]],
        experience=[ParsedWorkExperienceEntry(**e) for e in parsed["experience"]],
        skills=ParsedSkillsBreakdown(**parsed["skills"]),
        layout_metrics=LayoutMetrics(**formatting_eval_res["layout_metrics"])
    )
    
    jd_match_model = JDMatchDetail(**keyword_match_res["jd_match"]) if keyword_match_res.get("jd_match") else None
    role_match_model = RoleMatchDetail(**keyword_match_res["role_match"])
    unified_kw_model = UnifiedKeywordMatch(
        keyword_score=keyword_score,
        role_match=role_match_model,
        jd_match=jd_match_model
    )
    
    sec_completeness_model = SectionCompletenessDetail(**formatting_eval_res["section_completeness"])
    impact_model = ImpactEvaluationDetail(**formatting_eval_res["impact_evaluation"])
    formatting_model = FormattingEvaluation(
        formatting_score=formatting_score,
        section_completeness=sec_completeness_model,
        impact_evaluation=impact_model,
        layout_metrics=LayoutMetrics(**formatting_eval_res["layout_metrics"]),
        warnings=formatting_eval_res["warnings"]
    )
    
    applicant_id = str(uuid.uuid4())
    candidate_disp_name = parsed["contact"]["name"] or "Candidate"
    
    report = ResumeAnalysisReport(
        overall_score=overall_score,
        grade=grade,
        summary=f"{candidate_disp_name} exhibits a {grade} profile ({overall_score}% ATS match) for {role_info['title']}. Technical depth scored {skills_score}/100 with {metrics_score}% metric velocity.",
        category_scores=category_scores,
        skills=skills_groups,
        strengths=strengths,
        weaknesses=weaknesses,
        improvements=improvements,
        recommended_interview_topics=recommended_topics,
        applicant_id=applicant_id,
        target_role=resolved_role_key,
        parsed_data=parsed_model,
        keyword_matching=unified_kw_model,
        formatting_evaluation=formatting_model
    )
    
    # 9. Candidate Database Logging
    matched_skills_list = (
        keyword_match_res["jd_match"]["matched_keywords"]
        if keyword_match_res.get("jd_match")
        else keyword_match_res["role_match"]["matched_core_skills"] + parsed["skills"]["languages"]
    )
    missing_skills_list = (
        keyword_match_res["jd_match"]["missing_keywords"]
        if keyword_match_res.get("jd_match")
        else keyword_match_res["role_match"]["missing_core_skills"]
    )
    
    applicant_record = {
        "id": applicant_id,
        "candidate_name": candidate_disp_name,
        "email": parsed["contact"]["email"],
        "phone": parsed["contact"]["phone"],
        "target_role": resolved_role_key,
        "overall_score": overall_score,
        "grade": grade,
        "keyword_match_score": keyword_score,
        "formatting_score": formatting_score,
        "skills_match_score": skills_score,
        "matched_skills": matched_skills_list,
        "missing_skills": missing_skills_list,
        "created_at": datetime.now(timezone.utc),
        "raw_text": parsed["layout"]["full_text"]
    }
    
    # Save to memory cache
    IN_MEMORY_APPLICANTS[applicant_id] = applicant_record
    
    # Persist to PostgreSQL if connected
    if db:
        try:
            profile_id = None
            if user_id:
                profile_res = await db.execute(select(Profile).where(Profile.user_id == user_id))
                profile = profile_res.scalar_one_or_none()
                if profile:
                    profile_id = profile.id
                    
            db_report = ResumeReport(
                id=applicant_id,
                user_id=user_id,
                profile_id=profile_id,
                target_role=resolved_role_key,
                overall_score=overall_score,
                grade=grade,
                report_data=report.model_dump()
            )
            db.add(db_report)
            
            db_applicant = CandidateApplicant(
                id=applicant_id,
                resume_report_id=applicant_id,
                user_id=user_id,
                candidate_name=candidate_disp_name,
                email=parsed["contact"]["email"],
                phone=parsed["contact"]["phone"],
                target_role=resolved_role_key,
                job_description_snippet=(job_description[:300] if job_description else None),
                overall_score=overall_score,
                grade=grade,
                keyword_match_score=keyword_score,
                formatting_score=formatting_score,
                skills_match_score=skills_score,
                matched_skills=matched_skills_list,
                missing_skills=missing_skills_list,
                raw_details=parsed
            )
            db.add(db_applicant)
            await db.commit()
        except Exception as e:
            await db.rollback()
            print(f"Warning: could not persist candidate applicant to PostgreSQL: {e}")
            
    return report

async def get_all_candidate_applicants(db: AsyncSession | None = None) -> List[Dict[str, Any]]:
    """Retrieve all logged candidates from PostgreSQL or the in-memory applicant registry."""
    if db:
        try:
            res = await db.execute(select(CandidateApplicant).order_by(desc(CandidateApplicant.overall_score)))
            db_records = res.scalars().all()
            if db_records:
                return [
                    {
                        "id": r.id,
                        "candidate_name": r.candidate_name,
                        "email": r.email,
                        "phone": r.phone,
                        "target_role": r.target_role,
                        "overall_score": r.overall_score,
                        "grade": r.grade,
                        "keyword_match_score": r.keyword_match_score,
                        "formatting_score": r.formatting_score,
                        "matched_skills": r.matched_skills or [],
                        "missing_skills": r.missing_skills or [],
                        "created_at": r.created_at
                    }
                    for r in db_records
                ]
        except Exception as e:
            print(f"Notice: reading applicants from in-memory store ({e})")
            
    # In-memory fallback
    return list(IN_MEMORY_APPLICANTS.values())

async def rank_applicants(
    target_role: str | None = None,
    job_description: str | None = None,
    db: AsyncSession | None = None
) -> List[Dict[str, Any]]:
    """
    Score Assignment & Applicant Ranking:
    Calculates final match percentage against the target role or JD and ranks applicants
    from highest to lowest score.
    """
    all_applicants = await get_all_candidate_applicants(db)
    if not all_applicants:
        return []
        
    resolved_role = resolve_target_role(target_role) if target_role else None
    
    scored_applicants = []
    for app in all_applicants:
        # Base applicant metrics
        score = app.get("overall_score", 0)
        grade = app.get("grade", "B")
        matched = app.get("matched_skills", [])
        missing = app.get("missing_skills", [])
        kw_score = app.get("keyword_match_score", 0)
        
        # If a new custom Job Description is provided during ranking, re-match against JD
        if job_description and job_description.strip() and app.get("raw_text"):
            parsed_skills = {"all": matched}
            jd_res = match_resume_against_jd(app["raw_text"], parsed_skills, job_description)
            score = int(round((jd_res["match_percentage"] * 0.6) + (app.get("formatting_score", 75) * 0.4)))
            grade = assign_grade(score)
            matched = jd_res["matched_keywords"]
            missing = jd_res["missing_keywords"]
            kw_score = jd_res["match_percentage"]
            
        scored_applicants.append({
            "applicant_id": app["id"],
            "candidate_name": app.get("candidate_name", "Candidate"),
            "email": app.get("email"),
            "target_role": app.get("target_role", resolved_role or "sde"),
            "overall_score": score,
            "grade": grade,
            "keyword_match_score": kw_score,
            "formatting_score": app.get("formatting_score", 0),
            "matched_skills": matched,
            "missing_skills": missing
        })
        
    # Rank descending by overall score
    scored_applicants.sort(key=lambda x: x["overall_score"], reverse=True)
    
    ranked_list = []
    for rank_idx, applicant in enumerate(scored_applicants, start=1):
        item = dict(applicant)
        item["rank"] = rank_idx
        ranked_list.append(item)
        
    return ranked_list
