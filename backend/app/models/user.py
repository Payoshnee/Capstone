from sqlalchemy import String, Text, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base
from app.models.booking import ExpertProfile

class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    role: Mapped[str] = mapped_column(String, default="candidate", index=True)

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"
    user_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    target_role: Mapped[str | None] = mapped_column(String, nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    resume_url: Mapped[str | None] = mapped_column(String, nullable=True)
    resume_parsed_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
