"""Permission API routes."""
from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_permission_service
from app.models.user import User
from app.schemas.permission import PermissionCreate, PermissionResponse
from app.services.permission_service import PermissionService
from app.utils.responses import APIResponse

router = APIRouter()


@router.get("", response_model=APIResponse[list])
async def list_permissions(
    current_user: User = Depends(get_current_user),
    service: PermissionService = Depends(get_permission_service),
):
    """List all permissions."""
    perms = await service.get_all()
    data = [PermissionResponse(id=p.id, name=p.name, code=p.code, description=p.description) for p in perms]
    return APIResponse(data=data)


@router.post("", response_model=APIResponse[PermissionResponse], status_code=201)
async def create_permission(
    payload: PermissionCreate,
    current_user: User = Depends(get_current_user),
    service: PermissionService = Depends(get_permission_service),
):
    """Create a permission (admin)."""
    perm = await service.create(payload)
    return APIResponse(message="Permission created", data=PermissionResponse(id=perm.id, name=perm.name, code=perm.code, description=perm.description))
