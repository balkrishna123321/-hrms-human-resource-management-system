# HRMS Lite – API Overview

Base URL: `http://localhost:8000` (or your deployed backend).

All authenticated endpoints require header: `Authorization: Bearer <access_token>`.

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Login with `email`, `password`. Returns `access_token`, `refresh_token`. |
| POST | `/api/v1/auth/refresh` | Body: `refresh_token`. Returns new token pair. |
| GET | `/api/v1/auth/me` | Current user (requires Bearer token). |

## Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Service and database health (no auth). |
| GET | `/health` | Simple app health (no auth). |

## Employees

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/employees` | List employees (query: `page`, `per_page`, `department`, `department_id`, `is_active`). |
| GET | `/api/v1/employees/{id}` | Get one employee. |
| POST | `/api/v1/employees` | Create employee (see schema: employee_id, full_name, email, phone, department, department_id, designation, date_of_joining, manager_id, address, emergency_contact_*, date_of_birth, gender, employee_type). |
| PATCH | `/api/v1/employees/{id}` | Update employee (partial). |
| DELETE | `/api/v1/employees/{id}` | Delete employee. |

## Departments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/departments` | List departments (query: `page`, `per_page`). |
| GET | `/api/v1/departments/{id}` | Get one department. |
| POST | `/api/v1/departments` | Create department (name, code, description). |
| PATCH | `/api/v1/departments/{id}` | Update department (partial). |
| DELETE | `/api/v1/departments/{id}` | Delete department. |

## Attendance

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/attendance` | List all attendance (query: `page`, `per_page`, `from_date`, `to_date`, `status`, `department`). |
| GET | `/api/v1/attendance/employee/{id}` | List attendance for one employee (query: same + filters). |
| GET | `/api/v1/attendance/employee/{id}/present-days` | Total present days (query: `from_date`, `to_date`). |
| POST | `/api/v1/attendance/employee/{id}` | Mark attendance (date, status, check_in_time, check_out_time, work_hours, source, notes). |
| PATCH | `/api/v1/attendance/{id}` | Update attendance record. |
| DELETE | `/api/v1/attendance/{id}` | Delete attendance record. |

## Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dashboard/summary` | Counts: total_employees, total_attendance_records, present_count, absent_count (query: `from_date`, `to_date`). |
| GET | `/api/v1/dashboard/departments` | Departments with employee count. |

## Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/reports/attendance-summary` | Attendance counts by status in date range. |
| GET | `/api/v1/reports/employee-count-by-department` | Employee count per department. |

## Response format

- Success: `{ "success": true, "message": "...", "data": ... }`.
- Paginated: `{ "success": true, "data": [...], "meta": { "page", "per_page", "total", "total_pages", "has_next", "has_prev" } }`.
- Error: `{ "success": false, "message": "...", "error_code": "...", "details": [...] }`.

## Default admin (seeded)

- **Email**: `admin@hrms.local`
- **Password**: `admin123`

Use these to obtain an access token for testing. Change in production.
