from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_token
from app.schemas.booking import BookingCancel, BookingCreate, BookingResponse
from app.schemas.common import APIResponse
from app.services.booking_service import booking_service

router = APIRouter()


@router.post("", response_model=APIResponse[BookingResponse], status_code=201)
async def create_booking(
    payload: BookingCreate,
    claims: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    booking = await booking_service.create_booking(
        db, claims["sub"], claims.get("email"), payload.slot_id, payload.notes
    )
    return APIResponse(data=booking)


@router.get("/me", response_model=APIResponse[list[BookingResponse]])
async def list_my_bookings(
    view: Literal["candidate", "expert"] = Query(default="candidate"),
    claims: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    bookings = await booking_service.list_bookings(db, claims["sub"], view)
    return APIResponse(data=bookings)


@router.post("/{booking_id}/cancel", response_model=APIResponse[BookingResponse])
async def cancel_booking(
    booking_id: str,
    payload: BookingCancel,
    claims: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
):
    booking = await booking_service.cancel_booking(db, claims["sub"], booking_id, payload.reason)
    return APIResponse(data=booking)
