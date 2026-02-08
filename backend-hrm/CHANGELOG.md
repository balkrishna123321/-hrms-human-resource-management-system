# Changelog

All notable changes to the HRMS Lite Backend API are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.1.0] - 2025-02-07

### Added

- **Department model and CRUD**: Departments with name, code, description. Full REST API under `/api/v1/departments`.
- **Employee extended fields**: `phone`, `designation`, `date_of_joining`, `manager_id`, `address`, `emergency_contact_name`, `emergency_contact_phone`, `date_of_birth`, `gender`, `employee_type` (full_time, contract, intern, part_time), `department_id` (FK), `created_at`, `updated_at`.
- **Attendance extended fields**: `check_in_time`, `check_out_time`, `work_hours`, `source` (web, manual, biometric, api). New statuses: `half_day`, `on_leave`, `wfh`.
- **Health API**: `/api/v1/health` with database connectivity check.
- **Reports API**: `/api/v1/reports/attendance-summary`, `/api/v1/reports/employee-count-by-department`.
- **Seed**: Default departments (Engineering, HR, Operations, Sales, Finance) created on first run.
- **Makefile**: Targets for `run`, `install`, `test`, `lint`, `docker-build`.
- **Documentation**: CONTRIBUTING.md, docs/API.md.

### Changed

- Employee list supports filter by `department_id` in addition to `department` (string).
- Employee create/update accept all new fields and `department_id` for linking to Department.

## [1.0.0] - 2025-02-07

### Added

- Initial release: FastAPI, PostgreSQL (async), JWT + refresh token auth.
- Employee CRUD with pagination and filters.
- Attendance CRUD with date/status/department filters, present-days count.
- Dashboard summary and department breakdown.
- Generic API response, error response, pagination models.
- Default admin user seed: `admin@hrms.local` / `admin123`.
