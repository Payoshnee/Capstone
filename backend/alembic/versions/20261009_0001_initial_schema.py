"""Create users, profiles, resume reports, availability, and bookings.

Revision ID: 20261009_0001
Revises:
Create Date: 2026-10-09
"""

from typing import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "20261009_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def base_columns():
    return (
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def upgrade() -> None:
    op.create_table(
        "users",
        *base_columns(),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("role", sa.String(length=20), nullable=False, server_default="candidate"),
        sa.Column("password_hash", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "candidate_profiles",
        *base_columns(),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("target_role", sa.String(), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_candidate_profiles_user_id", "candidate_profiles", ["user_id"], unique=True)

    op.create_table(
        "expert_profiles",
        *base_columns(),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("domains", postgresql.ARRAY(sa.String()), nullable=False, server_default="{}"),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("company", sa.String(), nullable=True),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("approved", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_expert_profiles_user_id", "expert_profiles", ["user_id"], unique=True)
    op.create_index("ix_expert_profiles_approved", "expert_profiles", ["approved"])

    op.create_table(
        "resume_reports",
        *base_columns(),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("target_role", sa.String(), nullable=True),
        sa.Column("report_data", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_resume_reports_user_id", "resume_reports", ["user_id"])

    op.create_table(
        "availability_slots",
        *base_columns(),
        sa.Column("expert_id", sa.String(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_booked", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.CheckConstraint("end_time > start_time", name="ck_slot_positive_duration"),
        sa.ForeignKeyConstraint(["expert_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_availability_slots_expert_id", "availability_slots", ["expert_id"])
    op.create_index("ix_availability_slots_is_booked", "availability_slots", ["is_booked"])
    op.create_index("ix_slots_expert_start", "availability_slots", ["expert_id", "start_time"])

    op.create_table(
        "bookings",
        *base_columns(),
        sa.Column("candidate_id", sa.String(), nullable=False),
        sa.Column("expert_id", sa.String(), nullable=False),
        sa.Column("slot_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="scheduled"),
        sa.Column("session_type", sa.String(length=20), nullable=False, server_default="expert"),
        sa.Column("notes", sa.String(length=500), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancellation_reason", sa.String(length=300), nullable=True),
        sa.CheckConstraint(
            "status IN ('scheduled', 'completed', 'cancelled', 'no_show')",
            name="ck_booking_status",
        ),
        sa.ForeignKeyConstraint(["candidate_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["expert_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["slot_id"], ["availability_slots.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_bookings_candidate_id", "bookings", ["candidate_id"])
    op.create_index("ix_bookings_expert_id", "bookings", ["expert_id"])
    op.create_index("ix_bookings_status", "bookings", ["status"])
    op.create_index(
        "uq_booking_active_slot",
        "bookings",
        ["slot_id"],
        unique=True,
        postgresql_where=sa.text("status = 'scheduled'"),
    )
    op.create_index("ix_bookings_candidate_created", "bookings", ["candidate_id", "created_at"])
    op.create_index("ix_bookings_expert_created", "bookings", ["expert_id", "created_at"])


def downgrade() -> None:
    op.drop_table("bookings")
    op.drop_table("availability_slots")
    op.drop_table("resume_reports")
    op.drop_table("expert_profiles")
    op.drop_table("candidate_profiles")
    op.drop_table("users")
