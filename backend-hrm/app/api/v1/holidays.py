"""Holiday API routes."""
from datetime import date

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user, get_holiday_service
from app.models.user import User
from app.schemas.holiday import HolidayCreate, HolidayUpdate, HolidayResponse
from app.services.holiday_service import HolidayService
from app.utils.responses import APIResponse, PaginatedResponse, pagination_meta

router = APIRouter()


@router.get("", response_model=PaginatedResponse[HolidayResponse])
async def list_holidays(
    page: int = Query(1, ge=1),
    per_page: int = Query(100, ge=1, le=200),
    year: int | None = Query(None),
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
    current_user: User = Depends(get_current_user),
    service: HolidayService = Depends(get_holiday_service),
):
    items, total = await service.get_all(page=page, per_page=per_page, year=year, from_date=from_date, to_date=to_date)
    meta = pagination_meta(page, per_page, total)
    data = [HolidayResponse(id=h.id, name=h.name, date=h.date, year=h.year, description=h.description) for h in items]
    return PaginatedResponse(data=data, meta=meta)


@router.get("/{holiday_id}", response_model=APIResponse[HolidayResponse])
async def get_holiday(
    holiday_id: int,
    current_user: User = Depends(get_current_user),
    service: HolidayService = Depends(get_holiday_service),
):
    h = await service.get_by_id(holiday_id)
    return APIResponse(data=HolidayResponse(id=h.id, name=h.name, date=h.date, year=h.year, description=h.description))


@router.post("", response_model=APIResponse[HolidayResponse], status_code=201)
async def create_holiday(
    payload: HolidayCreate,
    current_user: User = Depends(get_current_user),
    service: HolidayService = Depends(get_holiday_service),
):
    h = await service.create(payload)
    return APIResponse(message="Holiday created", data=HolidayResponse(id=h.id, name=h.name, date=h.date, year=h.year, description=h.description))


@router.patch("/{holiday_id}", response_model=APIResponse[HolidayResponse])
async def update_holiday(
    holiday_id: int,
    payload: HolidayUpdate,
    current_user: User = Depends(get_current_user),
    service: HolidayService = Depends(get_holiday_service),
):
    h = await service.update(holiday_id, payload)
    return APIResponse(message="Holiday updated", data=HolidayResponse(id=h.id, name=h.name, date=h.date, year=h.year, description=h.description))


@router.delete("/{holiday_id}", status_code=204)
async def delete_holiday(
    holiday_id: int,
    current_user: User = Depends(get_current_user),
    service: HolidayService = Depends(get_holiday_service),
):
    await service.delete(holiday_id)
