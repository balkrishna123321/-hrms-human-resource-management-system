"""Employee business logic."""
from datetime import datetime, timezone

from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.department_repository import DepartmentRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.utils.exceptions import ConflictError, NotFoundError


class EmployeeService:
    """Employee use cases."""

    def __init__(self, repo: EmployeeRepository, department_repo: DepartmentRepository | None = None):
        self.repo = repo
        self.department_repo = department_repo

    def _department_name(self, employee: Employee) -> str | None:
        """Resolve department display name from relation or denormalized field."""
        if employee.department_rel:
            return employee.department_rel.name
        return employee.department

    async def get_by_id(self, id: int) -> Employee:
        """Get employee or raise NotFound."""
        employee = await self.repo.get_by_id(id)
        if not employee:
            raise NotFoundError("Employee not found", resource="employee_id")
        return employee

    async def get_all(
        self,
        page: int = 1,
        per_page: int = 20,
        department: str | None = None,
        department_id: int | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[Employee], int]:
        """Get paginated employees."""
        skip = (page - 1) * per_page
        return await self.repo.get_all(
            skip=skip,
            limit=per_page,
            department=department,
            department_id=department_id,
            is_active=is_active,
        )

    async def create(self, payload: EmployeeCreate) -> Employee:
        """Create employee; enforce unique employee_id and email."""
        if await self.repo.get_by_employee_id(payload.employee_id):
            raise ConflictError("Employee ID already exists", field="employee_id")
        if await self.repo.get_by_email(payload.email):
            raise ConflictError("Email already registered", field="email")
        department_name = payload.department
        if payload.department_id and self.department_repo:
            dept = await self.department_repo.get_by_id(payload.department_id)
            if dept:
                department_name = dept.name
        employee = Employee(
            employee_id=payload.employee_id,
            full_name=payload.full_name,
            email=payload.email,
            phone=payload.phone,
            department=department_name,
            department_id=payload.department_id,
            designation=payload.designation,
            date_of_joining=payload.date_of_joining,
            manager_id=payload.manager_id,
            address=payload.address,
            emergency_contact_name=payload.emergency_contact_name,
            emergency_contact_phone=payload.emergency_contact_phone,
            date_of_birth=payload.date_of_birth,
            gender=payload.gender,
            employee_type=payload.employee_type,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        return await self.repo.create(employee)

    async def update(self, id: int, payload: EmployeeUpdate) -> Employee:
        """Update employee; check email uniqueness if changed."""
        employee = await self.get_by_id(id)
        if payload.email is not None and payload.email != employee.email:
            if await self.repo.get_by_email(payload.email):
                raise ConflictError("Email already registered", field="email")
        if payload.full_name is not None:
            employee.full_name = payload.full_name
        if payload.email is not None:
            employee.email = payload.email
        if payload.phone is not None:
            employee.phone = payload.phone
        if payload.department is not None:
            employee.department = payload.department
        if payload.department_id is not None:
            employee.department_id = payload.department_id
            if self.department_repo:
                dept = await self.department_repo.get_by_id(payload.department_id)
                if dept:
                    employee.department = dept.name
        if payload.designation is not None:
            employee.designation = payload.designation
        if payload.date_of_joining is not None:
            employee.date_of_joining = payload.date_of_joining
        if payload.manager_id is not None:
            employee.manager_id = payload.manager_id
        if payload.address is not None:
            employee.address = payload.address
        if payload.emergency_contact_name is not None:
            employee.emergency_contact_name = payload.emergency_contact_name
        if payload.emergency_contact_phone is not None:
            employee.emergency_contact_phone = payload.emergency_contact_phone
        if payload.date_of_birth is not None:
            employee.date_of_birth = payload.date_of_birth
        if payload.gender is not None:
            employee.gender = payload.gender
        if payload.employee_type is not None:
            employee.employee_type = payload.employee_type
        if payload.is_active is not None:
            employee.is_active = payload.is_active
        employee.updated_at = datetime.now(timezone.utc)
        await self.repo.db.flush()
        await self.repo.db.refresh(employee)
        return employee

    async def delete(self, id: int) -> None:
        """Delete employee."""
        employee = await self.get_by_id(id)
        await self.repo.delete(employee)
