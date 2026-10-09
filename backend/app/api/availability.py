from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_token
from app.schemas.booking import AvailabilityBulkCreate, AvailabilityResponse
from app.schemas.common import APIResponse
from app.services.booking_service import booking_service

router = APIRouter()


def _response(slot) -> AvailabilityResponse:
    return AvailabilityResponse(
        id=slot.id,
        expert_id=slot.expert_id,
        start_time=slot.start_time,
        end_time=slot.end_time,
        is_booked=slot.is_booked,
    )


@router.post("", response_model=APIResponse[list[AvailabilityResponse]], status_code=201)
async def create_availability(
    payload: AvailabilityBulkCreate,
    claims: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    slots = await booking_service.create_slots(db, claims["sub"], payload.slots)
    return APIResponse(data=[_response(slot) for slot in slots])


@router.get("/experts/{expert_id}", response_model=APIResponse[list[AvailabilityResponse]])
async def list_availability(
    expert_id: str,
    start: datetime = Query(...),
    end: datetime = Query(...),
    include_booked: bool = False,
    db: AsyncSession = Depends(get_db),
):
    slots = await booking_service.list_slots(db, expert_id, start, end, include_booked)
    return APIResponse(data=[_response(slot) for slot in slots])


@router.delete("/{slot_id}", response_model=APIResponse[dict])
async def delete_availability(
    slot_id: str,
    claims: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    await booking_service.delete_slot(db, claims["sub"], slot_id)
    return APIResponse(data={"deleted": True})
