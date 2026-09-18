from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class ResumeScoreCategory(BaseModel):
    category_name: str
    score: int = Field(..., ge=0, le=100)
    weight: float = 0.25
    feedback_text: str

class ResumeSkillGroup(BaseModel):
    category: str
    skills: List[str]

class ResumeImprovement(BaseModel):
    section: str
    issue: str
    before_text: str
    suggested_text: str
    priority: str

# 1. Parsed Data Schemas
class ParsedContactInfo(BaseModel):
    name: str = "Candidate"
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    location: Optional[str] = None

class ParsedEducationEntry(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None
    gpa: Optional[str] = None

class ParsedWorkExperienceEntry(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    date_range: Optional[str] = None
    bullets: List[str] = []

class ParsedSkillsBreakdown(BaseModel):
    languages: List[str] = []
    frameworks_and_libraries: List[str] = []
    databases: List[str] = []
    cloud_and_devops: List[str] = []
    concepts_and_methodologies: List[str] = []

class LayoutMetrics(BaseModel):
    page_count: int = 1
    total_words: int = 0
    words_per_page: int = 0
    bullet_count: int = 0

class ParsedResumeData(BaseModel):
    contact: ParsedContactInfo
    education: List[ParsedEducationEntry] = []
    experience: List[ParsedWorkExperienceEntry] = []
    skills: ParsedSkillsBreakdown
    layout_metrics: LayoutMetrics

# 2. Keyword Matching Schemas
class JDMatchDetail(BaseModel):
    has_jd: bool = True
    total_jd_keywords: int = 0
    matched_count: int = 0
    missing_count: int = 0
    match_percentage: int = 0
    match_level: str = "Moderate Match"
    matched_keywords: List[str] = []
    missing_keywords: List[str] = []
    keyword_density: Dict[str, int] = {}

class RoleMatchDetail(BaseModel):
    role_key: str
    role_title: str
    track: str
    role_score: int
    matched_core_skills: List[str] = []
    missing_core_skills: List[str] = []
    matched_languages: List[str] = []
    missing_languages: List[str] = []
    matched_tools: List[str] = []
    missing_tools: List[str] = []
    recommended_interview_topics: List[str] = []

class UnifiedKeywordMatch(BaseModel):
    keyword_score: int
    role_match: RoleMatchDetail
    jd_match: Optional[JDMatchDetail] = None

# 3. Formatting Evaluation Schemas
class SectionCompletenessDetail(BaseModel):
    completeness_score: int
    checklist: Dict[str, bool]
    missing_sections: List[str] = []

class ImpactEvaluationDetail(BaseModel):
    total_bullets_analyzed: int
    bullets_with_action_verbs: int
    bullets_with_metrics: int
    action_verb_score: int
    quantified_metrics_score: int
    detected_action_verbs: List[str] = []

class FormattingEvaluation(BaseModel):
    formatting_score: int
    section_completeness: SectionCompletenessDetail
    impact_evaluation: ImpactEvaluationDetail
    layout_metrics: LayoutMetrics
    warnings: List[str] = []

# 4. Master ATS Report Schema (fully backwards-compatible)
class ResumeAnalysisReport(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    grade: str
    summary: str
    category_scores: List[ResumeScoreCategory]
    skills: List[ResumeSkillGroup]
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[ResumeImprovement]
    recommended_interview_topics: List[str]
    
    # Enriched fields for the complete ATS engine
    applicant_id: Optional[str] = None
    target_role: Optional[str] = None
    parsed_data: Optional[ParsedResumeData] = None
    keyword_matching: Optional[UnifiedKeywordMatch] = None
    formatting_evaluation: Optional[FormattingEvaluation] = None

# 5. Candidate Applicant & Ranking Schemas
class CandidateApplicantSchema(BaseModel):
    id: str
    candidate_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    target_role: str
    overall_score: int
    grade: str
    keyword_match_score: int
    formatting_score: int
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    created_at: Optional[datetime] = None

class ApplicantRankingItem(BaseModel):
    rank: int
    applicant_id: str
    candidate_name: str
    email: Optional[str] = None
    target_role: str
    overall_score: int
    grade: str
    keyword_match_score: int
    formatting_score: int
    matched_skills: List[str] = []
    missing_skills: List[str] = []

class ApplicantRankingResponse(BaseModel):
    target_role_or_jd: str
    total_applicants: int
    ranked_applicants: List[ApplicantRankingItem]

class RankApplicantsRequest(BaseModel):
    target_role: Optional[str] = None
    job_description: Optional[str] = None

class MatchJDRequest(BaseModel):
    resume_text: Optional[str] = None
    applicant_id: Optional[str] = None
    job_description: str
    target_role: Optional[str] = "sde"
