from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, CandidateProfile, ExpertProfile
from app.schemas.user import UserCreate, ProfileUpdate
from typing import Optional
from app.core.security import hash_password
from app.core.config import settings

class UserService:
    @staticmethod
    async def bootstrap_auth_user(db: AsyncSession | None, claims: dict) -> User:
        if not db:
            raise RuntimeError("Database is not configured")
        user_id = claims["sub"]
        email = claims.get("email")
        if not email:
            raise ValueError("Authenticated account has no email address")
        metadata = claims.get("user_metadata") or {}
        requested_role = metadata.get("requested_role", "candidate")
        role = requested_role if requested_role in ("candidate", "expert") else "candidate"
        user = await db.get(User, user_id)
        if not user:
            user = User(
                id=user_id,
                email=email,
                full_name=metadata.get("full_name"),
                role=role,
            )
            db.add(user)
            await db.flush()
            if role == "expert":
                db.add(ExpertProfile(user_id=user_id, approved=False, domains=[]))
            else:
                db.add(CandidateProfile(user_id=user_id))
            await db.commit()
            await db.refresh(user)
        return user

    @staticmethod
    async def get_by_email(db: AsyncSession | None, email: str) -> Optional[User]:
        if not db:
            return None
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(db: AsyncSession | None, user_in: UserCreate) -> User:
        if not db:
            raise RuntimeError("Database is not configured")
        existing = await UserService.get_by_email(db, user_in.email.lower().strip())
        if existing:
            raise ValueError("An account with this email already exists")
        user = User(
            email=user_in.email.lower().strip(),
            full_name=user_in.full_name,
            role=user_in.role,
            password_hash=hash_password(user_in.password),
        )
        try:
            db.add(user)
            await db.flush()
            if user.role == "expert":
                db.add(ExpertProfile(
                    user_id=user.id,
                    approved=settings.AUTO_APPROVE_EXPERTS,
                    domains=[],
                ))
            else:
                db.add(CandidateProfile(user_id=user.id))
            await db.commit()
            await db.refresh(user)
        except Exception:
            await db.rollback()
            raise
        return user

    @staticmethod
    async def get_candidate_profile(db: AsyncSession | None, user_id: str) -> Optional[CandidateProfile]:
        if not db:
            return CandidateProfile(user_id=user_id, target_role="Frontend Engineer", bio="Aspiring engineer")
        try:
            result = await db.execute(select(CandidateProfile).where(CandidateProfile.user_id == user_id))
            return result.scalar_one_or_none()
        except Exception:
            return CandidateProfile(user_id=user_id, target_role="Frontend Engineer", bio="Aspiring engineer")

    @staticmethod
    async def update_candidate_profile(db: AsyncSession | None, user_id: str, profile_in: ProfileUpdate) -> CandidateProfile:
        if not db:
            return CandidateProfile(user_id=user_id, target_role=profile_in.target_role, bio=profile_in.bio)
        try:
            result = await db.execute(select(CandidateProfile).where(CandidateProfile.user_id == user_id))
            profile = result.scalar_one_or_none()
            if not profile:
                profile = CandidateProfile(user_id=user_id, target_role=profile_in.target_role, bio=profile_in.bio)
                db.add(profile)
            else:
                if profile_in.target_role is not None:
                    profile.target_role = profile_in.target_role
                if profile_in.bio is not None:
                    profile.bio = profile_in.bio
            await db.commit()
            await db.refresh(profile)
            return profile
        except Exception:
            await db.rollback()
            return CandidateProfile(user_id=user_id, target_role=profile_in.target_role, bio=profile_in.bio)

user_service = UserService()
