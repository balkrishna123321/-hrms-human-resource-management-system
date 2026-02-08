# Changelog

All notable changes to the HRMS Lite Frontend are documented here.

## [1.1.0] - 2025-02-07

### Added

- **Login guidance**: On the login page, a clear note for first-time users: "Use default admin: admin@hrms.local / admin123" (seeded by the backend).
- **Departments page**: List, add, and delete departments; sidebar link to Departments.
- **Employee detail page**: View single employee profile, attendance summary (present days), and recent attendance list at `/employees/[id]`.
- **Extended employee form**: Add employee with phone, designation, date of joining, department (link or name), address, emergency contact, date of birth, employment type.
- **API types and endpoints**: DepartmentResponse, departments CRUD in `api.departments`; extended EmployeeResponse and attendance status/source types.
- **Makefile**: Targets for `install`, `dev`, `build`, `lint`, `docker-build`.

### Changed

- Employee list table: employee name links to detail page.
- API client: employees list supports `department_id` filter; create/update support all new fields.

## [1.0.0] - 2025-02-07

### Added

- Initial release: Next.js 16 (App Router), Shadcn UI, dark/light theme.
- Auth: login, JWT + refresh, protected dashboard layout.
- Dashboard: summary cards, department list.
- Employees: list (paginated), add, delete.
- Attendance: mark form, list with date/status filters.
