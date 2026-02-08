"""Role API routes."""
from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user, get_role_service
from app.models.user import User
from app.schemas.permission import PermissionResponse
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse, RoleWithPermissionsResponse
from app.services.role_service import RoleService
from app.utils.responses import APIResponse, PaginatedResponse, pagination_meta

router = APIRouter()


@router.get("", response_model=PaginatedResponse[RoleWithPermissionsResponse])
async def list_roles(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    service: RoleService = Depends(get_role_service),
):
    """List roles with their permissions."""
    items, total = await service.get_all(page=page, per_page=per_page)
    meta = pagination_meta(page, per_page, total)
    data = [
        RoleWithPermissionsResponse(
            id=r.id,
            name=r.name,
            code=r.code,
            description=r.description,
            permissions=[PermissionResponse(id=p.id, name=p.name, code=p.code, description=p.description) for p in r.permissions],
        )
        for r in items
    ]
    return PaginatedResponse(data=data, meta=meta)


@router.get("/{role_id}", response_model=APIResponse[RoleWithPermissionsResponse])
async def get_role(
    role_id: int,
    current_user: User = Depends(get_current_user),
    service: RoleService = Depends(get_role_service),
):
    """Get role by id with permissions."""
    role = await service.get_by_id(role_id)
    return APIResponse(
        data=RoleWithPermissionsResponse(
            id=role.id,
            name=role.name,
            code=role.code,
            description=role.description,
            permissions=[PermissionResponse(id=p.id, name=p.name, code=p.code, description=p.description) for p in role.permissions],
        )
    )


@router.post("", response_model=APIResponse[RoleResponse], status_code=201)
async def create_role(
    payload: RoleCreate,
    current_user: User = Depends(get_current_user),
    service: RoleService = Depends(get_role_service),
):
    """Create a role with permissions."""
    role = await service.create(payload)
    return APIResponse(message="Role created", data=RoleResponse(id=role.id, name=role.name, code=role.code, description=role.description))


@router.patch("/{role_id}", response_model=APIResponse[RoleWithPermissionsResponse])
async def update_role(
    role_id: int,
    payload: RoleUpdate,
    current_user: User = Depends(get_current_user),
    service: RoleService = Depends(get_role_service),
):
    """Update role (including permissions)."""
    role = await service.update(role_id, payload)
    return APIResponse(
        message="Role updated",
        data=RoleWithPermissionsResponse(
            id=role.id,
            name=role.name,
            code=role.code,
            description=role.description,
            permissions=[PermissionResponse(id=p.id, name=p.name, code=p.code, description=p.description) for p in role.permissions],
        ),
    )


@router.delete("/{role_id}", status_code=204)
async def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_user),
    service: RoleService = Depends(get_role_service),
):
    """Delete a role."""
    await service.delete(role_id)
