from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import AvailabilitySlot, Booking
from app.models.user import ExpertProfile, User
from app.schemas.booking import AvailabilityCreate, BookingResponse


class BookingError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _utc(value: datetime) -> datetime:
    return value.astimezone(timezone.utc)


def _booking_response(booking: Booking, slot: AvailabilitySlot) -> BookingResponse:
    return BookingResponse(
        id=booking.id,
        candidate_id=booking.candidate_id,
        expert_id=booking.expert_id,
        slot_id=booking.slot_id,
        status=booking.status,
        session_type=booking.session_type,
        notes=booking.notes,
        start_time=slot.start_time,
        end_time=slot.end_time,
        created_at=booking.created_at,
        cancelled_at=booking.cancelled_at,
        cancellation_reason=booking.cancellation_reason,
    )


class BookingService:
    async def _require_db(self, db: AsyncSession | None) -> AsyncSession:
        if db is None:
            raise BookingError("Database is not configured", 503)
        return db

    async def _require_expert(self, db: AsyncSession, expert_id: str) -> None:
        result = await db.execute(
            select(ExpertProfile).where(
                ExpertProfile.user_id == expert_id,
                ExpertProfile.approved.is_(True),
            )
        )
        if not result.scalar_one_or_none():
            raise BookingError("Only approved experts can manage availability", 403)

    async def create_slots(
        self, db: AsyncSession | None, expert_id: str, items: list[AvailabilityCreate]
    ) -> list[AvailabilitySlot]:
        db = await self._require_db(db)
        await self._require_expert(db, expert_id)
        now = datetime.now(timezone.utc)
        normalized = [(_utc(item.start_time), _utc(item.end_time)) for item in items]
        normalized.sort(key=lambda item: item[0])

        for index, (start, end) in enumerate(normalized):
            if start <= now:
                raise BookingError("Availability must start in the future")
            if end - start < timedelta(minutes=15) or end - start > timedelta(hours=4):
                raise BookingError("Slots must be between 15 minutes and 4 hours")
            if index and start < normalized[index - 1][1]:
                raise BookingError("Submitted availability slots overlap")

        # Serialize slot creation per expert. This prevents concurrent overlap checks
        # from both succeeding in PostgreSQL.
        await db.execute(select(User).where(User.id == expert_id).with_for_update())
        earliest, latest = normalized[0][0], max(end for _, end in normalized)
        existing = await db.execute(
            select(AvailabilitySlot).where(
                AvailabilitySlot.expert_id == expert_id,
                AvailabilitySlot.start_time < latest,
                AvailabilitySlot.end_time > earliest,
            )
        )
        existing_slots = existing.scalars().all()
        for start, end in normalized:
            if any(slot.start_time < end and slot.end_time > start for slot in existing_slots):
                raise BookingError("Availability overlaps an existing slot", 409)

        slots = [
            AvailabilitySlot(expert_id=expert_id, start_time=start, end_time=end)
            for start, end in normalized
        ]
        db.add_all(slots)
        await db.commit()
        for slot in slots:
            await db.refresh(slot)
        return slots

    async def list_slots(
        self,
        db: AsyncSession | None,
        expert_id: str,
        start: datetime,
        end: datetime,
        include_booked: bool,
    ) -> list[AvailabilitySlot]:
        db = await self._require_db(db)
        if end <= start or end - start > timedelta(days=93):
            raise BookingError("Date range must be positive and no longer than 93 days")
        conditions = [
            AvailabilitySlot.expert_id == expert_id,
            AvailabilitySlot.start_time >= _utc(start),
            AvailabilitySlot.start_time < _utc(end),
        ]
        if not include_booked:
            conditions.append(AvailabilitySlot.is_booked.is_(False))
        result = await db.execute(
            select(AvailabilitySlot).where(*conditions).order_by(AvailabilitySlot.start_time)
        )
        return list(result.scalars().all())

    async def delete_slot(self, db: AsyncSession | None, expert_id: str, slot_id: str) -> None:
        db = await self._require_db(db)
        slot = await db.scalar(
            select(AvailabilitySlot)
            .where(AvailabilitySlot.id == slot_id, AvailabilitySlot.expert_id == expert_id)
            .with_for_update()
        )
        if not slot:
            raise BookingError("Availability slot not found", 404)
        if slot.is_booked:
            raise BookingError("A booked slot cannot be deleted; cancel the booking instead", 409)
        await db.delete(slot)
        await db.commit()

    async def create_booking(
        self,
        db: AsyncSession | None,
        candidate_id: str,
        candidate_email: str | None,
        slot_id: str,
        notes: str | None,
    ) -> BookingResponse:
        db = await self._require_db(db)
        candidate = await db.get(User, candidate_id)
        if not candidate:
            candidate = User(
                id=candidate_id,
                email=candidate_email or f"{candidate_id}@supabase.local",
                role="candidate",
            )
            db.add(candidate)
            await db.flush()
        slot = await db.scalar(
            select(AvailabilitySlot).where(AvailabilitySlot.id == slot_id).with_for_update()
        )
        if not slot:
            raise BookingError("Availability slot not found", 404)
        if slot.is_booked:
            raise BookingError("This slot has already been booked", 409)
        if slot.start_time <= datetime.now(timezone.utc):
            raise BookingError("This slot is no longer available", 409)
        if slot.expert_id == candidate_id:
            raise BookingError("Experts cannot book their own availability")

        booking = Booking(
            candidate_id=candidate_id,
            expert_id=slot.expert_id,
            slot_id=slot.id,
            notes=notes,
        )
        slot.is_booked = True
        db.add(booking)
        try:
            await db.commit()
            await db.refresh(booking)
        except IntegrityError:
            await db.rollback()
            raise BookingError("This slot has already been booked", 409)
        return _booking_response(booking, slot)

    async def list_bookings(
        self, db: AsyncSession | None, user_id: str, view: str
    ) -> list[BookingResponse]:
        db = await self._require_db(db)
        owner_clause = Booking.expert_id == user_id if view == "expert" else Booking.candidate_id == user_id
        result = await db.execute(
            select(Booking, AvailabilitySlot)
            .join(AvailabilitySlot, AvailabilitySlot.id == Booking.slot_id)
            .where(owner_clause)
            .order_by(AvailabilitySlot.start_time.desc())
        )
        return [_booking_response(booking, slot) for booking, slot in result.all()]

    async def cancel_booking(
        self, db: AsyncSession | None, user_id: str, booking_id: str, reason: str | None
    ) -> BookingResponse:
        db = await self._require_db(db)
        result = await db.execute(
            select(Booking, AvailabilitySlot)
            .join(AvailabilitySlot, AvailabilitySlot.id == Booking.slot_id)
            .where(Booking.id == booking_id)
            .with_for_update()
        )
        row = result.one_or_none()
        if not row:
            raise BookingError("Booking not found", 404)
        booking, slot = row
        if user_id not in (booking.candidate_id, booking.expert_id):
            raise BookingError("You cannot cancel this booking", 403)
        if booking.status != "scheduled":
            raise BookingError("Only scheduled bookings can be cancelled", 409)
        if slot.start_time <= datetime.now(timezone.utc):
            raise BookingError("Past bookings cannot be cancelled", 409)

        booking.status = "cancelled"
        booking.cancelled_at = datetime.now(timezone.utc)
        booking.cancellation_reason = reason
        slot.is_booked = False
        await db.commit()
        await db.refresh(booking)
        return _booking_response(booking, slot)


booking_service = BookingService()
