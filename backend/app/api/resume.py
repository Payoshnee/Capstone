"""
Compatibility router forwarding to the isolated resume_review microservice module.
"""
from app.services.resume_review.api import router

__all__ = ["router"]

