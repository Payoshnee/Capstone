"""
Keyword Matching Engine for ATS Scoring.
Compares extracted candidate resume text and skills against a target Job Description
or standardized SDE / Data role profiles to identify matches, gaps, and density.
"""
import re
from typing import Dict, List, Any, Set, Tuple
from app.services.resume_review.keyword_pool import (
    ROLE_PROFILES,
    resolve_target_role,
    PROGRAMMING_LANGUAGES,
    FRAMEWORKS_AND_LIBRARIES,
    DATABASES_AND_STORAGE,
    CLOUD_AND_DEVOPS,
    CORE_CONCEPTS
)

ALL_KNOWN_TECH_KEYWORDS: Set[str] = (
    PROGRAMMING_LANGUAGES 
    | FRAMEWORKS_AND_LIBRARIES 
    | DATABASES_AND_STORAGE 
    | CLOUD_AND_DEVOPS 
    | CORE_CONCEPTS
)

def extract_keywords_from_jd(jd_text: str) -> List[str]:
    """Extract recognized technical keywords, tools, and concepts from a Job Description."""
    jd_lower = jd_text.lower()
    extracted = set()
    
    for kw in ALL_KNOWN_TECH_KEYWORDS:
        escaped = re.escape(kw)
        pattern = rf'(?:\b|(?<=\s)){escaped}(?:\b|(?=\s|,|\.|\/|\)))'
        if re.search(pattern, jd_lower):
            extracted.add(kw)
            
    return sorted(list(extracted))

def calculate_keyword_density(resume_text: str, keywords: List[str]) -> Dict[str, int]:
    """Calculate the occurrence count of each keyword in the resume text."""
    text_lower = resume_text.lower()
    density = {}
    for kw in keywords:
        escaped = re.escape(kw)
        matches = re.findall(rf'(?:\b|(?<=\s)){escaped}(?:\b|(?=\s|,|\.|\/|\)))', text_lower)
        if matches:
            density[kw] = len(matches)
    return density

def match_resume_against_role(
    resume_text: str,
    parsed_skills: Dict[str, List[str]],
    target_role_key: str
) -> Dict[str, Any]:
    """Match resume text against a predefined standard role profile in keyword_pool."""
    role_key = resolve_target_role(target_role_key)
    profile = ROLE_PROFILES.get(role_key, ROLE_PROFILES["sde"])
    
    text_lower = resume_text.lower()
    
    # Check core skills
    matched_core = []
    missing_core = []
    for skill in profile["core_skills"]:
        escaped = re.escape(skill)
        if re.search(rf'(?:\b|(?<=\s)){escaped}(?:\b|(?=\s|,|\.|\/|\)))', text_lower):
            matched_core.append(skill)
        else:
            missing_core.append(skill)
            
    # Check core languages
    matched_langs = []
    missing_langs = []
    for lang in profile["core_languages"]:
        escaped = re.escape(lang)
        if re.search(rf'(?:\b|(?<=\s)){escaped}(?:\b|(?=\s|,|\.|\/|\)))', text_lower):
            matched_langs.append(lang)
        else:
            missing_langs.append(lang)
            
    # Check preferred tools
    matched_tools = []
    missing_tools = []
    for tool in profile["preferred_tools"]:
        escaped = re.escape(tool)
        if re.search(rf'(?:\b|(?<=\s)){escaped}(?:\b|(?=\s|,|\.|\/|\)))', text_lower):
            matched_tools.append(tool)
        else:
            missing_tools.append(tool)
            
    # Calculate role alignment score
    core_score = (len(matched_core) / max(1, len(profile["core_skills"]))) * 50
    lang_score = (min(len(matched_langs), 2) / 2) * 25  # at least 2 relevant languages
    tool_score = (len(matched_tools) / max(1, len(profile["preferred_tools"]))) * 25
    
    role_score = int(round(core_score + lang_score + tool_score))
    
    return {
        "role_key": role_key,
        "role_title": profile["title"],
        "track": profile["track"],
        "role_score": min(100, max(0, role_score)),
        "matched_core_skills": matched_core,
        "missing_core_skills": missing_core,
        "matched_languages": matched_langs,
        "missing_languages": missing_langs,
        "matched_tools": matched_tools,
        "missing_tools": missing_tools,
        "recommended_interview_topics": profile.get("recommended_topics", [])
    }

def match_resume_against_jd(
    resume_text: str,
    parsed_skills: Dict[str, List[str]],
    job_description: str
) -> Dict[str, Any]:
    """Compare resume text directly against an input Job Description."""
    jd_keywords = extract_keywords_from_jd(job_description)
    if not jd_keywords:
        # Fallback if JD text doesn't contain recognized keywords: extract nouns/tokens
        words = [w.strip(".,;:()[]{}") for w in job_description.lower().split() if len(w) > 3]
        jd_keywords = sorted(list(set(words[:15])))
        
    text_lower = resume_text.lower()
    matched = []
    missing = []
    
    for kw in jd_keywords:
        escaped = re.escape(kw)
        if re.search(rf'(?:\b|(?<=\s)){escaped}(?:\b|(?=\s|,|\.|\/|\)))', text_lower):
            matched.append(kw)
        else:
            missing.append(kw)
            
    total_required = max(1, len(jd_keywords))
    match_percentage = int(round((len(matched) / total_required) * 100))
    match_percentage = min(100, max(0, match_percentage))
    
    if match_percentage >= 75:
        match_level = "High Match"
    elif match_percentage >= 50:
        match_level = "Moderate Match"
    else:
        match_level = "Low Match"
        
    density = calculate_keyword_density(resume_text, matched)
    
    return {
        "has_jd": True,
        "total_jd_keywords": len(jd_keywords),
        "matched_count": len(matched),
        "missing_count": len(missing),
        "match_percentage": match_percentage,
        "match_level": match_level,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "keyword_density": density
    }

def perform_keyword_matching(
    resume_text: str,
    parsed_skills: Dict[str, List[str]],
    target_role: str | None = None,
    job_description: str | None = None
) -> Dict[str, Any]:
    """Unified keyword matching pipeline matching against JD and/or role profile."""
    role_match = match_resume_against_role(resume_text, parsed_skills, target_role or "sde")
    
    jd_match = None
    if job_description and job_description.strip():
        jd_match = match_resume_against_jd(resume_text, parsed_skills, job_description)
        
    # Compute keyword matching composite score
    if jd_match:
        keyword_score = int(round((jd_match["match_percentage"] * 0.7) + (role_match["role_score"] * 0.3)))
    else:
        keyword_score = role_match["role_score"]
        
    return {
        "keyword_score": min(100, max(0, keyword_score)),
        "role_match": role_match,
        "jd_match": jd_match
    }
