"""Department API routes."""
from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_department_service, get_current_user
from app.models.user import User
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.services.department_service import DepartmentService
from app.utils.responses import APIResponse, PaginatedResponse, pagination_meta

router = APIRouter()


@router.get("", response_model=PaginatedResponse[DepartmentResponse])
async def list_departments(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: DepartmentService = Depends(get_department_service),
):
    """List all departments with pagination."""
    items, total = await service.get_all(page=page, per_page=per_page)
    meta = pagination_meta(page, per_page, total)
    data = [
        DepartmentResponse(id=d.id, name=d.name, code=d.code, description=d.description)
        for d in items
    ]
    return PaginatedResponse(data=data, meta=meta)


@router.get("/{department_id}", response_model=APIResponse[DepartmentResponse])
async def get_department(
    department_id: int,
    current_user: User = Depends(get_current_user),
    service: DepartmentService = Depends(get_department_service),
):
    """Get a single department by id."""
    department = await service.get_by_id(department_id)
    return APIResponse(
        data=DepartmentResponse(id=department.id, name=department.name, code=department.code, description=department.description),
    )


@router.post("", response_model=APIResponse[DepartmentResponse], status_code=201)
async def create_department(
    payload: DepartmentCreate,
    current_user: User = Depends(get_current_user),
    service: DepartmentService = Depends(get_department_service),
):
    """Create a new department."""
    department = await service.create(payload)
    return APIResponse(
        message="Department created",
        data=DepartmentResponse(id=department.id, name=department.name, code=department.code, description=department.description),
    )


@router.patch("/{department_id}", response_model=APIResponse[DepartmentResponse])
async def update_department(
    department_id: int,
    payload: DepartmentUpdate,
    current_user: User = Depends(get_current_user),
    service: DepartmentService = Depends(get_department_service),
):
    """Update a department (partial)."""
    department = await service.update(department_id, payload)
    return APIResponse(
        message="Department updated",
        data=DepartmentResponse(id=department.id, name=department.name, code=department.code, description=department.description),
    )


@router.delete("/{department_id}", status_code=204)
async def delete_department(
    department_id: int,
    current_user: User = Depends(get_current_user),
    service: DepartmentService = Depends(get_department_service),
):
    """Delete a department."""
    await service.delete(department_id)
