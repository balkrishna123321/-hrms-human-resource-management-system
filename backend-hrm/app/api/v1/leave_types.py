"""Leave type API routes."""
from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user, get_leave_type_service
from app.models.user import User
from app.schemas.leave_type import LeaveTypeCreate, LeaveTypeUpdate, LeaveTypeResponse
from app.services.leave_type_service import LeaveTypeService
from app.utils.responses import APIResponse, PaginatedResponse, pagination_meta

router = APIRouter()


@router.get("", response_model=PaginatedResponse[LeaveTypeResponse])
async def list_leave_types(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: LeaveTypeService = Depends(get_leave_type_service),
):
    items, total = await service.get_all(page=page, per_page=per_page)
    meta = pagination_meta(page, per_page, total)
    data = [
        LeaveTypeResponse(id=lt.id, name=lt.name, code=lt.code, default_days_per_year=lt.default_days_per_year, description=lt.description)
        for lt in items
    ]
    return PaginatedResponse(data=data, meta=meta)


@router.get("/{leave_type_id}", response_model=APIResponse[LeaveTypeResponse])
async def get_leave_type(
    leave_type_id: int,
    current_user: User = Depends(get_current_user),
    service: LeaveTypeService = Depends(get_leave_type_service),
):
    lt = await service.get_by_id(leave_type_id)
    return APIResponse(data=LeaveTypeResponse(id=lt.id, name=lt.name, code=lt.code, default_days_per_year=lt.default_days_per_year, description=lt.description))


@router.post("", response_model=APIResponse[LeaveTypeResponse], status_code=201)
async def create_leave_type(
    payload: LeaveTypeCreate,
    current_user: User = Depends(get_current_user),
    service: LeaveTypeService = Depends(get_leave_type_service),
):
    lt = await service.create(payload)
    return APIResponse(message="Leave type created", data=LeaveTypeResponse(id=lt.id, name=lt.name, code=lt.code, default_days_per_year=lt.default_days_per_year, description=lt.description))


@router.patch("/{leave_type_id}", response_model=APIResponse[LeaveTypeResponse])
async def update_leave_type(
    leave_type_id: int,
    payload: LeaveTypeUpdate,
    current_user: User = Depends(get_current_user),
    service: LeaveTypeService = Depends(get_leave_type_service),
):
    lt = await service.update(leave_type_id, payload)
    return APIResponse(message="Leave type updated", data=LeaveTypeResponse(id=lt.id, name=lt.name, code=lt.code, default_days_per_year=lt.default_days_per_year, description=lt.description))


@router.delete("/{leave_type_id}", status_code=204)
async def delete_leave_type(
    leave_type_id: int,
    current_user: User = Depends(get_current_user),
    service: LeaveTypeService = Depends(get_leave_type_service),
):
    await service.delete(leave_type_id)
