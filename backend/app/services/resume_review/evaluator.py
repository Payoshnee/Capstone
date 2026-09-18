"""
Formatting & ATS Structure Evaluation Engine.
Evaluates section completeness, layout readability, bullet rhythm,
action verb density, and quantifiable impact metrics for ATS scoring.
"""
import re
from typing import Dict, List, Any
from app.services.resume_review.keyword_pool import ALL_ACTION_VERBS

METRIC_REGEX = re.compile(r'(?:\b\d+(?:\.\d+)?%|\$\d+(?:,\d{3})*(?:\.\d+)?|\b\d+(?:,\d{3})*\b|\b\d+[kKmMbB]\+?|\b\d+x\b|\b(?:reduced|increased|improved|cut|saved|scaled)\s+(?:by\s+)?\d+)', re.IGNORECASE)

def evaluate_section_completeness(
    contact: Dict[str, Any],
    sections: Dict[str, str],
    extracted_skills: Dict[str, List[str]]
) -> Dict[str, Any]:
    """Check for the presence and validity of standard resume sections."""
    has_contact = bool(contact.get("email") and (contact.get("phone") or contact.get("linkedin") or contact.get("github")))
    has_experience = bool(sections.get("experience", "").strip())
    has_education = bool(sections.get("education", "").strip())
    
    total_skills = sum(len(v) for v in extracted_skills.values())
    has_skills = bool(sections.get("skills", "").strip()) or total_skills >= 4
    
    has_projects = bool(sections.get("projects", "").strip())
    has_summary = bool(sections.get("summary", "").strip())
    has_certifications = bool(sections.get("certifications", "").strip())
    
    # Point distribution (100 total)
    # Contact: 20, Experience: 30, Education: 20, Skills: 15, Projects: 15
    score = 0
    if has_contact:
        score += 20
    if has_experience:
        score += 30
    if has_education:
        score += 20
    if has_skills:
        score += 15
    if has_projects:
        score += 15
        
    checklist = {
        "contact_info": has_contact,
        "work_experience": has_experience,
        "education": has_education,
        "skills": has_skills,
        "projects": has_projects,
        "summary": has_summary,
        "certifications": has_certifications
    }
    
    missing_sections = [k.replace("_", " ").title() for k, v in checklist.items() if not v and k in ["contact_info", "work_experience", "education", "skills", "projects"]]
    
    return {
        "completeness_score": score,
        "checklist": checklist,
        "missing_sections": missing_sections
    }

def evaluate_bullet_points_and_impact(
    bullet_lines: List[str],
    experience_text: str
) -> Dict[str, Any]:
    """Analyze action verb density and quantifiable metrics across resume bullets."""
    bullets = bullet_lines
    if not bullets:
        # Fallback: split experience lines into sentences
        exp_lines = [l.strip() for l in experience_text.splitlines() if len(l.strip()) > 20]
        bullets = exp_lines
        
    total_bullets = max(1, len(bullets))
    
    verbs_matched = []
    bullets_with_verb = 0
    bullets_with_metrics = 0
    
    for bullet in bullets:
        cleaned = re.sub(r'^[•\-*▪–—\d\.\)]\s*', '', bullet).strip().lower()
        words = cleaned.split()
        
        # Check first 3 words for action verbs
        has_verb = False
        for word in words[:3]:
            # Strip punctuation
            w_clean = re.sub(r'[^a-zA-Z]', '', word)
            if w_clean in ALL_ACTION_VERBS:
                verbs_matched.append(w_clean)
                has_verb = True
                break
        if has_verb:
            bullets_with_verb += 1
            
        # Check for quantifiable metrics
        if METRIC_REGEX.search(bullet):
            bullets_with_metrics += 1
            
    verb_ratio = int(round((bullets_with_verb / total_bullets) * 100))
    metric_ratio = int(round((bullets_with_metrics / total_bullets) * 100))
    
    return {
        "total_bullets_analyzed": len(bullets),
        "bullets_with_action_verbs": bullets_with_verb,
        "bullets_with_metrics": bullets_with_metrics,
        "action_verb_score": min(100, max(0, verb_ratio)),
        "quantified_metrics_score": min(100, max(0, metric_ratio)),
        "detected_action_verbs": sorted(list(set(verbs_matched)))
    }

def evaluate_formatting_and_layout(
    layout: Dict[str, Any],
    contact: Dict[str, Any],
    sections: Dict[str, str],
    extracted_skills: Dict[str, List[str]]
) -> Dict[str, Any]:
    """Calculate overall formatting & structure score with detailed feedback and warnings."""
    sec_eval = evaluate_section_completeness(contact, sections, extracted_skills)
    bullet_eval = evaluate_bullet_points_and_impact(layout.get("bullet_lines", []), sections.get("experience", ""))
    
    warnings = []
    
    # 1. Page density & length
    page_count = layout.get("page_count", 1)
    total_words = layout.get("total_words", 0)
    words_per_page = total_words / max(1, page_count)
    
    layout_score = 100
    if page_count > 2:
        warnings.append(f"Resume is {page_count} pages long. For most tech candidates, a 1-page (or max 2-page) resume is recommended.")
        layout_score -= 15
    if total_words < 200:
        warnings.append("Resume content is sparse (<200 words). Add detailed project and work experience bullets.")
        layout_score -= 25
    elif words_per_page > 1100:
        warnings.append("High text density (>1100 words/page). Ensure adequate whitespace for human reviewers and ATS readability.")
        layout_score -= 10
        
    # 2. Contact Warnings
    if not contact.get("email"):
        warnings.append("No email address detected. Contact information must be clearly visible.")
    if not contact.get("phone"):
        warnings.append("No phone number detected.")
    if not contact.get("linkedin") and not contact.get("github"):
        warnings.append("No LinkedIn or GitHub profile link found. Adding technical profiles significantly enhances ATS ranking.")
        
    # 3. Bullets and Metrics Warnings
    if bullet_eval["total_bullets_analyzed"] < 3:
        warnings.append("Few or no bullet points detected. Use bullet points instead of dense paragraphs for work history.")
        layout_score -= 15
    if bullet_eval["action_verb_score"] < 40:
        warnings.append("Low action verb usage. Begin bullets with impactful verbs (e.g., 'Architected', 'Optimized', 'Engineered').")
    if bullet_eval["quantified_metrics_score"] < 35:
        warnings.append("Missing quantifiable impact. Include numbers, percentages, and metrics to demonstrate outcomes (e.g. 'reduced latency by 35%').")

    # Composite formatting score
    # Completeness (35%), Action Verbs (25%), Metrics (25%), Layout (15%)
    raw_score = (
        (sec_eval["completeness_score"] * 0.35)
        + (bullet_eval["action_verb_score"] * 0.25)
        + (bullet_eval["quantified_metrics_score"] * 0.25)
        + (layout_score * 0.15)
    )
    
    final_score = int(round(raw_score))
    final_score = min(100, max(0, final_score))
    
    return {
        "formatting_score": final_score,
        "section_completeness": sec_eval,
        "impact_evaluation": bullet_eval,
        "layout_metrics": {
            "page_count": page_count,
            "total_words": total_words,
            "words_per_page": int(round(words_per_page)),
            "bullet_count": layout.get("bullet_count", 0)
        },
        "warnings": warnings
    }
