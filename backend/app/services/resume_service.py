"""
Compatibility layer forwarding calls to the isolated resume_review microservice module.
"""
from app.services.resume_review.service import (
    extract_text_from_pdf,
    analyze_resume
)

__all__ = ["extract_text_from_pdf", "analyze_resume"]

