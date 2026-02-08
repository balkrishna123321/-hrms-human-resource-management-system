"""Seed default admin user, roles, permissions, departments, leave types, holidays, and dummy data (~30/table)."""
import random
from datetime import date, datetime, time, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User
from app.models.department import Department
from app.models.permission import Permission
from app.models.role import Role
from app.models.leave_type import LeaveType
from app.models.holiday import Holiday
from app.models.employee import Employee, EmployeeType, Gender
from app.models.leave_balance import LeaveBalance
from app.models.leave_request import LeaveRequest, LeaveRequestStatus
from app.models.attendance import Attendance, AttendanceStatus, AttendanceSource

from app.db.seed_data import (
    EXTRA_PERMISSIONS,
    EXTRA_ROLES,
    EXTRA_DEPARTMENTS,
    EXTRA_LEAVE_TYPES,
    get_holiday_list,
    random_name,
    random_email,
    random_phone,
    random_date,
    DESIGNATIONS,
    STREETS,
    CITIES,
)


async def seed_permissions(session: AsyncSession) -> None:
    """Create default permissions if none exist."""
    result = await session.execute(select(Permission).limit(1))
    if result.scalar_one_or_none() is not None:
        return
    defaults = [
        Permission(name="Edit Employees", code="employee:edit", description="Create and update employees"),
        Permission(name="Delete Employees", code="employee:delete", description="Delete employees"),
        Permission(name="Mark Attendance", code="attendance:mark", description="Mark attendance"),
        Permission(name="Approve Leave", code="leave:approve", description="Approve or reject leave requests"),
        Permission(name="Manage Roles", code="role:manage", description="Manage roles and permissions"),
        Permission(name="Manage Holidays", code="holiday:manage", description="Manage holidays"),
    ]
    for p in defaults:
        session.add(p)
    await session.commit()


async def seed_roles(session: AsyncSession) -> None:
    """Create admin role with all permissions if no role exists."""
    result = await session.execute(select(Role).limit(1))
    if result.scalar_one_or_none() is not None:
        return
    perms_result = await session.execute(select(Permission))
    perms = list(perms_result.scalars().all())
    admin_role = Role(name="Administrator", code="admin", description="Full access")
    admin_role.permissions = perms
    session.add(admin_role)
    await session.commit()


async def seed_admin(session: AsyncSession) -> None:
    """Create default admin if no user exists and assign admin role."""
    result = await session.execute(select(User).limit(1))
    if result.scalar_one_or_none() is not None:
        return
    admin_role = await session.execute(select(Role).where(Role.code == "admin"))
    role = admin_role.scalar_one_or_none()
    admin = User(
        email="admin@hrms.local",
        hashed_password=get_password_hash("admin123"),
        full_name="HRMS Admin",
        role_id=role.id if role else None,
        is_active=True,
        is_superuser=True,
    )
    session.add(admin)
    await session.commit()


async def seed_departments(session: AsyncSession) -> None:
    """Create default departments if none exist."""
    result = await session.execute(select(Department).limit(1))
    if result.scalar_one_or_none() is not None:
        return
    defaults = [
        Department(name="Engineering", code="ENG", description="Software and product development"),
        Department(name="Human Resources", code="HR", description="HR operations and people"),
        Department(name="Operations", code="OPS", description="Business operations"),
        Department(name="Sales", code="SALES", description="Sales and business development"),
        Department(name="Finance", code="FIN", description="Finance and accounting"),
    ]
    for d in defaults:
        session.add(d)
    await session.commit()


async def seed_leave_types(session: AsyncSession) -> None:
    """Create default leave types if none exist."""
    result = await session.execute(select(LeaveType).limit(1))
    if result.scalar_one_or_none() is not None:
        return
    defaults = [
        LeaveType(name="Annual Leave", code="ANNUAL", default_days_per_year=20, description="Annual leave"),
        LeaveType(name="Sick Leave", code="SICK", default_days_per_year=10, description="Sick leave"),
        LeaveType(name="Personal Leave", code="PERSONAL", default_days_per_year=5, description="Personal leave"),
    ]
    for lt in defaults:
        session.add(lt)
    await session.commit()


async def seed_holidays(session: AsyncSession) -> None:
    """Create sample holidays if none exist."""
    result = await session.execute(select(Holiday).limit(1))
    if result.scalar_one_or_none() is not None:
        return
    year = date.today().year
    defaults = [
        Holiday(name="New Year", date=date(year, 1, 1), year=year),
        Holiday(name="Republic Day", date=date(year, 1, 26), year=year),
        Holiday(name="Independence Day", date=date(year, 8, 15), year=year),
    ]
    for h in defaults:
        session.add(h)
    await session.commit()


# --- Dummy data fill: ~30 records per table ---

async def seed_fill_permissions(session: AsyncSession) -> None:
    """Add extra permissions up to ~12."""
    result = await session.execute(select(func.count(Permission.id)))
    if result.scalar() >= 12:
        return
    existing = await session.execute(select(Permission.code))
    codes = {r[0] for r in existing.fetchall()}
    for name, code, desc in EXTRA_PERMISSIONS:
        if code in codes:
            continue
        session.add(Permission(name=name, code=code, description=desc))
        codes.add(code)
    await session.commit()


async def seed_fill_roles(session: AsyncSession) -> None:
    """Add extra roles up to ~10 and assign permissions."""
    result = await session.execute(select(func.count(Role.id)))
    if result.scalar() >= 10:
        return
    existing = await session.execute(select(Role.code))
    role_codes = {r[0] for r in existing.fetchall()}
    perms_result = await session.execute(select(Permission))
    all_perms = list(perms_result.scalars().all())
    for name, code, desc in EXTRA_ROLES:
        if code in role_codes:
            continue
        r = Role(name=name, code=code, description=desc)
        view_perms = [p for p in all_perms if "view" in p.code]
        if code == "manager":
            r.permissions = [p for p in all_perms if p.code in ("leave:approve", "attendance:mark", "attendance:view", "employee:edit", "report:view")]
        elif code == "hr_staff":
            r.permissions = [p for p in all_perms if "employee" in p.code or "holiday" in p.code or "leave" in p.code or "department" in p.code]
        elif code == "employee":
            r.permissions = view_perms[:4] if view_perms else all_perms[:2]
        else:
            r.permissions = view_perms[:6] if view_perms else all_perms[:3]
        if not r.permissions:
            r.permissions = all_perms[:2]
        session.add(r)
        role_codes.add(code)
    await session.commit()


async def seed_fill_departments(session: AsyncSession) -> None:
    """Add extra departments up to ~15."""
    result = await session.execute(select(func.count(Department.id)))
    if result.scalar() >= 15:
        return
    existing = await session.execute(select(Department.code))
    codes = {r[0] for r in existing.fetchall()}
    for name, code, desc in EXTRA_DEPARTMENTS:
        if code in codes:
            continue
        session.add(Department(name=name, code=code, description=desc))
        codes.add(code)
    await session.commit()


async def seed_fill_leave_types(session: AsyncSession) -> None:
    """Add extra leave types up to ~10."""
    result = await session.execute(select(func.count(LeaveType.id)))
    if result.scalar() >= 10:
        return
    existing = await session.execute(select(LeaveType.code))
    codes = {r[0] for r in existing.fetchall()}
    for name, code, days, desc in EXTRA_LEAVE_TYPES:
        if code in codes:
            continue
        session.add(LeaveType(name=name, code=code, default_days_per_year=days, description=desc))
        codes.add(code)
    await session.commit()


async def seed_fill_holidays(session: AsyncSession) -> None:
    """Add holidays up to ~25 for current year."""
    year = date.today().year
    result = await session.execute(select(func.count(Holiday.id)).where(Holiday.year == year))
    if result.scalar() >= 25:
        return
    existing = await session.execute(select(Holiday.date).where(Holiday.year == year))
    existing_dates = {r[0] for r in existing.fetchall()}
    for name, d in get_holiday_list(year):
        if d in existing_dates:
            continue
        session.add(Holiday(name=name, date=d, year=year))
        existing_dates.add(d)
    await session.commit()


async def seed_employees_dummy(session: AsyncSession) -> None:
    """Add ~30 employees with departments and managers."""
    result = await session.execute(select(func.count(Employee.id)))
    count = result.scalar() or 0
    if count >= 30:
        return
    depts = (await session.execute(select(Department))).scalars().all()
    if not depts:
        return
    need = 30 - count
    existing = await session.execute(select(Employee.employee_id))
    used_emp_ids = {r[0] for r in existing.fetchall()}
    existing_email = await session.execute(select(Employee.email))
    used_emails = {r[0] for r in existing_email.fetchall()}
    today = date.today()
    join_start = today - timedelta(days=365 * 3)
    employees_added = []
    for i in range(need):
        full_name = random_name()
        email = random_email(full_name, used_emails)
        n = len(used_emp_ids) + 1
        emp_id = f"EMP{n:04d}"
        while emp_id in used_emp_ids:
            n += 1
            emp_id = f"EMP{n:04d}"
        used_emp_ids.add(emp_id)
        dept = depts[i % len(depts)]
        designation = DESIGNATIONS[i % len(DESIGNATIONS)]
        emp = Employee(
            employee_id=emp_id,
            full_name=full_name,
            email=email,
            phone=random_phone(),
            department=dept.name,
            department_id=dept.id,
            designation=designation,
            date_of_joining=random_date(join_start, today),
            manager_id=None,
            address=f"{random.randint(1, 99)} {STREETS[i % len(STREETS)]}, {CITIES[i % len(CITIES)]}",
            emergency_contact_name=random_name(),
            emergency_contact_phone=random_phone(),
            date_of_birth=random_date(date(today.year - 45, 1, 1), date(today.year - 22, 12, 31)),
            gender=[Gender.MALE, Gender.FEMALE][i % 2],
            employee_type=[EmployeeType.FULL_TIME, EmployeeType.CONTRACT, EmployeeType.INTERN][i % 3] if i > 2 else EmployeeType.FULL_TIME,
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(emp)
        await session.flush()
        employees_added.append(emp)
    # Set managers: first 3 of this batch as managers, rest report to them
    if len(employees_added) >= 3:
        manager_ids = [employees_added[0].id, employees_added[1].id, employees_added[2].id]
        for idx, e in enumerate(employees_added[3:], start=3):
            e.manager_id = manager_ids[idx % 3]
    await session.commit()


async def seed_leave_balances_dummy(session: AsyncSession) -> None:
    """Create leave balances for current year for each employee and leave type."""
    year = date.today().year
    employees = (await session.execute(select(Employee))).scalars().all()
    leave_types = (await session.execute(select(LeaveType))).scalars().all()
    if not employees or not leave_types:
        return
    existing = await session.execute(
        select(LeaveBalance.employee_id, LeaveBalance.leave_type_id).where(LeaveBalance.year == year)
    )
    existing_pairs = {(r[0], r[1]) for r in existing.fetchall()}
    for emp in employees:
        for lt in leave_types:
            if (emp.id, lt.id) in existing_pairs:
                continue
            balance_days = lt.default_days_per_year
            used = 0
            if balance_days > 0:
                used = min(balance_days, 5)
            session.add(
                LeaveBalance(
                    employee_id=emp.id,
                    leave_type_id=lt.id,
                    year=year,
                    balance_days=balance_days,
                    used_days=used,
                )
            )
    await session.commit()


async def seed_leave_requests_dummy(session: AsyncSession) -> None:
    """Add ~30 leave requests with mixed statuses."""
    result = await session.execute(select(func.count(LeaveRequest.id)))
    count = result.scalar() or 0
    if count >= 30:
        return
    employees = (await session.execute(select(Employee).limit(50))).scalars().all()
    leave_types = (await session.execute(select(LeaveType))).scalars().all()
    users = (await session.execute(select(User).limit(5))).scalars().all()
    if not employees or not leave_types:
        return
    need = 30 - count
    today = date.today()
    statuses = [LeaveRequestStatus.PENDING, LeaveRequestStatus.APPROVED, LeaveRequestStatus.REJECTED, LeaveRequestStatus.CANCELLED]
    for _ in range(need):
        emp = employees[_ % len(employees)]
        lt = leave_types[_ % len(leave_types)]
        from_d = random_date(today - timedelta(days=60), today + timedelta(days=90))
        to_d = from_d + timedelta(days=min(random.randint(1, 5), 10))
        status = statuses[_ % len(statuses)]
        session.add(
            LeaveRequest(
                employee_id=emp.id,
                leave_type_id=lt.id,
                from_date=from_d,
                to_date=to_d,
                status=status,
                reason="Family event" if _ % 3 == 0 else "Personal" if _ % 3 == 1 else "Medical",
                approved_by_id=users[0].id if users and status == LeaveRequestStatus.APPROVED else None,
            )
        )
    await session.commit()


async def seed_attendance_dummy(session: AsyncSession) -> None:
    """Add attendance for last 30 days for each employee."""
    today = date.today()
    start = today - timedelta(days=30)
    employees = (await session.execute(select(Employee))).scalars().all()
    if not employees:
        return
    existing = await session.execute(
        select(Attendance.employee_id, Attendance.date).where(Attendance.date >= start)
    )
    existing_pairs = {(r[0], r[1]) for r in existing.fetchall()}
    statuses = [AttendanceStatus.PRESENT, AttendanceStatus.PRESENT, AttendanceStatus.WFH, AttendanceStatus.HALF_DAY, AttendanceStatus.ABSENT, AttendanceStatus.ON_LEAVE]
    for emp in employees:
        for d in (start + timedelta(days=i) for i in range(31)):
            if d > today or (emp.id, d) in existing_pairs:
                continue
            status = statuses[(emp.id + d.toordinal()) % len(statuses)]
            check_in = time(9, 0, 0) if status in (AttendanceStatus.PRESENT, AttendanceStatus.WFH, AttendanceStatus.HALF_DAY) else None
            check_out = time(18, 0, 0) if status == AttendanceStatus.PRESENT else (time(13, 0, 0) if status == AttendanceStatus.HALF_DAY else None)
            work_hrs = 9.0 if status == AttendanceStatus.PRESENT else (4.5 if status == AttendanceStatus.HALF_DAY else None)
            session.add(
                Attendance(
                    employee_id=emp.id,
                    date=d,
                    status=status,
                    check_in_time=check_in,
                    check_out_time=check_out,
                    work_hours=work_hrs,
                    source=AttendanceSource.WEB,
                )
            )
    await session.commit()
