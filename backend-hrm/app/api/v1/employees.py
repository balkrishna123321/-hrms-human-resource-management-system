"""Employee API routes."""
from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_employee_service, get_current_user
from app.models.user import User
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse,
)
from app.services.employee_service import EmployeeService
from app.utils.responses import APIResponse, PaginatedResponse, pagination_meta

router = APIRouter()


def _employee_to_response(employee, department_name: str | None = None):
    """Build EmployeeResponse from model."""
    return EmployeeResponse(
        id=employee.id,
        employee_id=employee.employee_id,
        full_name=employee.full_name,
        email=employee.email,
        phone=employee.phone,
        department=employee.department or department_name,
        department_id=employee.department_id,
        designation=employee.designation,
        date_of_joining=employee.date_of_joining,
        manager_id=employee.manager_id,
        address=employee.address,
        emergency_contact_name=employee.emergency_contact_name,
        emergency_contact_phone=employee.emergency_contact_phone,
        date_of_birth=employee.date_of_birth,
        gender=employee.gender,
        employee_type=employee.employee_type,
        is_active=employee.is_active,
    )


@router.get("", response_model=PaginatedResponse[EmployeeListResponse])
async def list_employees(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=500),
    department: str | None = Query(None),
    department_id: int | None = Query(None),
    is_active: bool | None = Query(None),
    current_user: User = Depends(get_current_user),
    service: EmployeeService = Depends(get_employee_service),
):
    """List employees with pagination and optional filters."""
    items, total = await service.get_all(
        page=page,
        per_page=per_page,
        department=department,
        department_id=department_id,
        is_active=is_active,
    )
    meta = pagination_meta(page, per_page, total)
    data = []
    for e in items:
        dept_name = e.department
        base = _employee_to_response(e, dept_name)
        data.append(
            EmployeeListResponse(
                **base.model_dump(),
                total_present_days=None,
                department_name=dept_name,
            )
        )
    return PaginatedResponse(data=data, meta=meta)


@router.get("/{employee_id}", response_model=APIResponse[EmployeeResponse])
async def get_employee(
    employee_id: int,
    current_user: User = Depends(get_current_user),
    service: EmployeeService = Depends(get_employee_service),
):
    """Get single employee by id."""
    employee = await service.get_by_id(employee_id)
    dept_name = employee.department
    return APIResponse(
        data=_employee_to_response(employee, dept_name),
    )


@router.post("", response_model=APIResponse[EmployeeResponse], status_code=201)
async def create_employee(
    payload: EmployeeCreate,
    current_user: User = Depends(get_current_user),
    service: EmployeeService = Depends(get_employee_service),
):
    """Create a new employee."""
    employee = await service.create(payload)
    return APIResponse(
        message="Employee created",
        data=_employee_to_response(employee, employee.department),
    )


@router.patch("/{employee_id}", response_model=APIResponse[EmployeeResponse])
async def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    current_user: User = Depends(get_current_user),
    service: EmployeeService = Depends(get_employee_service),
):
    """Update employee (partial)."""
    employee = await service.update(employee_id, payload)
    return APIResponse(
        message="Employee updated",
        data=_employee_to_response(employee, employee.department),
    )


@router.delete("/{employee_id}", status_code=204)
async def delete_employee(
    employee_id: int,
    current_user: User = Depends(get_current_user),
    service: EmployeeService = Depends(get_employee_service),
):
    """Delete an employee."""
    await service.delete(employee_id)
