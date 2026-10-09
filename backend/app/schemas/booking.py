from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class AvailabilityCreate(BaseModel):
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_times(self):
        if self.start_time.tzinfo is None or self.end_time.tzinfo is None:
            raise ValueError("start_time and end_time must include a timezone")
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class AvailabilityBulkCreate(BaseModel):
    slots: list[AvailabilityCreate] = Field(min_length=1, max_length=50)


class AvailabilityResponse(BaseModel):
    id: str
    expert_id: str
    start_time: datetime
    end_time: datetime
    is_booked: bool


class BookingCreate(BaseModel):
    slot_id: str
    notes: str | None = Field(default=None, max_length=500)


class BookingCancel(BaseModel):
    reason: str | None = Field(default=None, max_length=300)


class BookingResponse(BaseModel):
    id: str
    candidate_id: str
    expert_id: str
    slot_id: str
    status: Literal["scheduled", "completed", "cancelled", "no_show"]
    session_type: str
    notes: str | None
    start_time: datetime
    end_time: datetime
    created_at: datetime
    cancelled_at: datetime | None
    cancellation_reason: str | None
