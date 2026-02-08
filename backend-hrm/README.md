# HRMS Lite – Backend

FastAPI-based REST API for HRMS Lite: employee management, attendance tracking, JWT auth, and dashboard summaries.

## Tech Stack

- **Python 3.11**, **FastAPI**, **SQLAlchemy 2 (async)**, **PostgreSQL** (asyncpg)
- **JWT** (access + refresh tokens), **Pydantic**, **Poetry**

## Project Structure

```
backend-hrm/
├── app/
│   ├── main.py              # FastAPI app, CORS, exception handlers
│   ├── core/                # Config, security (JWT), dependencies
│   ├── api/v1/               # API routes (auth, employees, attendance, dashboard)
│   ├── models/               # SQLAlchemy models (User, Employee, Attendance)
│   ├── schemas/              # Pydantic request/response schemas
│   ├── repositories/        # Data access layer
│   ├── services/            # Business logic
│   ├── db/                   # Engine, session, base, seed
│   └── utils/                # Generic API/error/pagination responses, exceptions
├── pyproject.toml
├── Dockerfile
└── README.md
```

## Features

- **Auth**: Login (email/password), refresh token, `GET /api/v1/auth/me`
- **Employees**: CRUD, list with pagination and filters (department, is_active)
- **Attendance**: Mark attendance (date, Present/Absent), list by employee or global, filters by date/status/department, update/delete
- **Dashboard**: Summary (employee count, attendance counts), department breakdown
- **Generic responses**: `APIResponse[T]`, `APIErrorResponse`, `PaginatedResponse[T]` with `PaginationMeta`
- **Validation**: Required fields, email format, duplicate employee ID/email handled with clear errors

## Run Locally

### Prerequisites

- Python 3.11+
- Poetry
- PostgreSQL (or use root `docker-compose` for Postgres)

### 1. Start Postgres (from repo root)

```bash
cd ..
docker compose up -d postgres
```

### 2. Backend

```bash
cd backend-hrm
poetry install
cp .env.example .env   # edit if needed
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API: http://localhost:8000  
Docs: http://localhost:8000/docs  

### Default admin (seeded on first run)

- **Email:** `admin@hrms.local`
- **Password:** `admin123`

## Environment

See `.env.example`. Main variables:

- `DATABASE_URL` – PostgreSQL async URL, e.g. `postgresql+asyncpg://hrms_user:hrms_secret@localhost:5432/hrms_db`
- `SECRET_KEY` – JWT signing key (min 32 chars in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
- `CORS_ORIGINS` – Allowed frontend origins

## Run with Docker

From repo root, you can extend `docker-compose.yml` with a `backend` service that uses this Dockerfile and `DATABASE_URL` pointing to the `postgres` service. Or build/run from here:

```bash
docker build -t hrms-backend .
docker run --env-file .env -p 8000:8000 --add-host=host.docker.internal:host-gateway hrms-backend
```

(Use `host.docker.internal` in `DATABASE_URL` to reach Postgres on host.)

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/login` | Login (email, password) → access + refresh tokens |
| POST | `/api/v1/auth/refresh` | Refresh tokens |
| GET | `/api/v1/auth/me` | Current user (requires Bearer token) |
| GET | `/api/v1/employees` | List employees (paginated, optional filters) |
| GET | `/api/v1/employees/{id}` | Get employee |
| POST | `/api/v1/employees` | Create employee |
| PATCH | `/api/v1/employees/{id}` | Update employee |
| DELETE | `/api/v1/employees/{id}` | Delete employee |
| GET | `/api/v1/attendance` | List all attendance (filters) |
| GET | `/api/v1/attendance/employee/{id}` | List attendance for employee |
| GET | `/api/v1/attendance/employee/{id}/present-days` | Total present days |
| POST | `/api/v1/attendance/employee/{id}` | Mark attendance |
| PATCH | `/api/v1/attendance/{id}` | Update attendance |
| DELETE | `/api/v1/attendance/{id}` | Delete attendance |
| GET | `/api/v1/dashboard/summary` | Dashboard counts |
| GET | `/api/v1/dashboard/departments` | Department summary |

All protected routes require header: `Authorization: Bearer <access_token>`.
