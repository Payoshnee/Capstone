from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class AvailabilitySlot(Base):
    __tablename__ = "availability_slots"
    __table_args__ = (
        CheckConstraint("end_time > start_time", name="ck_slot_positive_duration"),
        Index("ix_slots_expert_start", "expert_id", "start_time"),
    )

    expert_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_booked: Mapped[bool] = mapped_column(Boolean, default=False, index=True)


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        Index(
            "uq_booking_active_slot",
            "slot_id",
            unique=True,
            postgresql_where=text("status = 'scheduled'"),
        ),
        CheckConstraint(
            "status IN ('scheduled', 'completed', 'cancelled', 'no_show')",
            name="ck_booking_status",
        ),
        Index("ix_bookings_candidate_created", "candidate_id", "created_at"),
        Index("ix_bookings_expert_created", "expert_id", "created_at"),
    )

    candidate_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    expert_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    slot_id: Mapped[str] = mapped_column(String, ForeignKey("availability_slots.id", ondelete="RESTRICT"))
    status: Mapped[str] = mapped_column(String(20), default="scheduled", index=True)
    session_type: Mapped[str] = mapped_column(String(20), default="expert")
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancellation_reason: Mapped[str | None] = mapped_column(String(300), nullable=True)
