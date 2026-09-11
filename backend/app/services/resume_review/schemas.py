from pydantic import BaseModel, Field
from typing import List, Optional

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
