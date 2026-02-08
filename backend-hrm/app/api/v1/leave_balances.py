"""Leave balance API routes."""
from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user, get_leave_balance_service
from app.models.user import User
from app.schemas.leave_balance import LeaveBalanceCreate, LeaveBalanceUpdate, LeaveBalanceWithDetailsResponse
from app.services.leave_balance_service import LeaveBalanceService
from app.utils.responses import APIResponse, PaginatedResponse, pagination_meta

router = APIRouter()


@router.get("", response_model=PaginatedResponse[LeaveBalanceWithDetailsResponse])
async def list_leave_balances(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    employee_id: int | None = Query(None),
    year: int | None = Query(None),
    current_user: User = Depends(get_current_user),
    service: LeaveBalanceService = Depends(get_leave_balance_service),
):
    items, total = await service.get_all(page=page, per_page=per_page, employee_id=employee_id, year=year)
    meta = pagination_meta(page, per_page, total)
    data = []
    for lb in items:
        data.append(
            LeaveBalanceWithDetailsResponse(
                id=lb.id,
                employee_id=lb.employee_id,
                leave_type_id=lb.leave_type_id,
                year=lb.year,
                balance_days=lb.balance_days,
                used_days=lb.used_days,
                employee_name=lb.employee.full_name if lb.employee else None,
                leave_type_name=lb.leave_type.name if lb.leave_type else None,
                available_days=lb.balance_days - lb.used_days,
            )
        )
    return PaginatedResponse(data=data, meta=meta)


@router.get("/employee/{employee_id}", response_model=APIResponse[list])
async def get_employee_leave_balances(
    employee_id: int,
    year: int = Query(..., ge=2000, le=2100),
    current_user: User = Depends(get_current_user),
    service: LeaveBalanceService = Depends(get_leave_balance_service),
):
    """Get leave balances for an employee for a year."""
    items, _ = await service.get_all(employee_id=employee_id, year=year, per_page=100)
    data = [
        {
            "id": lb.id,
            "leave_type_id": lb.leave_type_id,
            "leave_type_name": lb.leave_type.name if lb.leave_type else None,
            "year": lb.year,
            "balance_days": lb.balance_days,
            "used_days": lb.used_days,
            "available_days": lb.balance_days - lb.used_days,
        }
        for lb in items
    ]
    return APIResponse(data=data)


@router.post("", response_model=APIResponse[LeaveBalanceWithDetailsResponse], status_code=201)
async def create_leave_balance(
    payload: LeaveBalanceCreate,
    current_user: User = Depends(get_current_user),
    service: LeaveBalanceService = Depends(get_leave_balance_service),
):
    lb = await service.create(payload)
    return APIResponse(
        message="Leave balance created",
        data=LeaveBalanceWithDetailsResponse(
            id=lb.id,
            employee_id=lb.employee_id,
            leave_type_id=lb.leave_type_id,
            year=lb.year,
            balance_days=lb.balance_days,
            used_days=lb.used_days,
            employee_name=lb.employee.full_name if lb.employee else None,
            leave_type_name=lb.leave_type.name if lb.leave_type else None,
            available_days=lb.balance_days - lb.used_days,
        ),
    )


@router.patch("/{balance_id}", response_model=APIResponse[LeaveBalanceWithDetailsResponse])
async def update_leave_balance(
    balance_id: int,
    payload: LeaveBalanceUpdate,
    current_user: User = Depends(get_current_user),
    service: LeaveBalanceService = Depends(get_leave_balance_service),
):
    lb = await service.update(balance_id, payload)
    lb = await service.get_by_id(lb.id)
    return APIResponse(
        message="Leave balance updated",
        data=LeaveBalanceWithDetailsResponse(
            id=lb.id,
            employee_id=lb.employee_id,
            leave_type_id=lb.leave_type_id,
            year=lb.year,
            balance_days=lb.balance_days,
            used_days=lb.used_days,
            employee_name=lb.employee.full_name if lb.employee else None,
            leave_type_name=lb.leave_type.name if lb.leave_type else None,
            available_days=lb.balance_days - lb.used_days,
        ),
    )
