"""Leave request API routes."""
from datetime import date

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user, get_leave_request_service
from app.models.user import User
from app.models.leave_request import LeaveRequestStatus
from app.schemas.leave_request import LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestWithDetailsResponse
from app.services.leave_request_service import LeaveRequestService
from app.utils.responses import APIResponse, PaginatedResponse, pagination_meta

router = APIRouter()


def _details(lr) -> dict:
    total_days = (lr.to_date - lr.from_date).days + 1
    return LeaveRequestWithDetailsResponse(
        id=lr.id,
        employee_id=lr.employee_id,
        leave_type_id=lr.leave_type_id,
        from_date=lr.from_date,
        to_date=lr.to_date,
        status=lr.status,
        reason=lr.reason,
        approved_by_id=lr.approved_by_id,
        employee_name=lr.employee.full_name if lr.employee else None,
        leave_type_name=lr.leave_type.name if lr.leave_type else None,
        total_days=total_days,
    )


@router.get("", response_model=PaginatedResponse[LeaveRequestWithDetailsResponse])
async def list_leave_requests(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    employee_id: int | None = Query(None),
    status: LeaveRequestStatus | None = Query(None),
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
    current_user: User = Depends(get_current_user),
    service: LeaveRequestService = Depends(get_leave_request_service),
):
    items, total = await service.get_all(page=page, per_page=per_page, employee_id=employee_id, status=status, from_date=from_date, to_date=to_date)
    meta = pagination_meta(page, per_page, total)
    data = [_details(lr) for lr in items]
    return PaginatedResponse(data=data, meta=meta)


@router.get("/{request_id}", response_model=APIResponse[LeaveRequestWithDetailsResponse])
async def get_leave_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    service: LeaveRequestService = Depends(get_leave_request_service),
):
    lr = await service.get_by_id(request_id)
    return APIResponse(data=_details(lr))


@router.post("/employee/{employee_id}", response_model=APIResponse[LeaveRequestWithDetailsResponse], status_code=201)
async def create_leave_request(
    employee_id: int,
    payload: LeaveRequestCreate,
    current_user: User = Depends(get_current_user),
    service: LeaveRequestService = Depends(get_leave_request_service),
):
    """Apply for leave (as employee)."""
    lr = await service.create(employee_id, payload)
    lr = await service.get_by_id(lr.id)
    return APIResponse(message="Leave request submitted", data=_details(lr))


@router.patch("/{request_id}", response_model=APIResponse[LeaveRequestWithDetailsResponse])
async def update_leave_request(
    request_id: int,
    payload: LeaveRequestUpdate,
    current_user: User = Depends(get_current_user),
    service: LeaveRequestService = Depends(get_leave_request_service),
):
    """Approve/reject or update leave request."""
    lr = await service.update(request_id, payload, approved_by_id=current_user.id)
    lr = await service.get_by_id(lr.id)
    return APIResponse(message="Leave request updated", data=_details(lr))


@router.delete("/{request_id}", status_code=204)
async def cancel_leave_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    service: LeaveRequestService = Depends(get_leave_request_service),
):
    """Cancel a leave request (set status to cancelled)."""
    await service.update(request_id, LeaveRequestUpdate(status=LeaveRequestStatus.CANCELLED), approved_by_id=current_user.id)
