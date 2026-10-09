from sqlalchemy import String, Text, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
from app.models.booking import ExpertProfile

class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default="candidate", index=True)  # candidate, mentor, team_admin, super_admin

class Profile(Base):
    __tablename__ = "profiles"
    user_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String, nullable=True)
    target_role: Mapped[str | None] = mapped_column(String, nullable=True)
    experience_level: Mapped[str | None] = mapped_column(String, default="mid")  # junior, mid, senior
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    resume_url: Mapped[str | None] = mapped_column(String, nullable=True)
    resume_parsed_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_companies: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    skills: Mapped[dict | None] = mapped_column(JSON, nullable=True)

# For backward compatibility
CandidateProfile = Profile

class Institution(Base):
    __tablename__ = "institutions"
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    type: Mapped[str] = mapped_column(String, default="university")  # university, bootcamp, corporate
    admin_user_id: Mapped[str] = mapped_column(String, index=True)

class InstitutionMember(Base):
    __tablename__ = "institution_members"
    institution_id: Mapped[str] = mapped_column(String, index=True)
    user_id: Mapped[str] = mapped_column(String, index=True)
    batch_name: Mapped[str | None] = mapped_column(String, nullable=True)  # e.g., "Class of 2026"
    status: Mapped[str] = mapped_column(String, default="active")  # active, graduated, pending
