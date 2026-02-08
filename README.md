# HRMS Lite

Full-stack Human Resource Management System: employee management, attendance tracking, JWT auth, dashboard, and optional Docker setup.

## Overview

- **Frontend**: Next.js 16 (App Router), TypeScript, Shadcn UI, dark/light theme, pnpm
- **Backend**: FastAPI, SQLAlchemy 2 (async), PostgreSQL, Poetry
- **Auth**: JWT access + refresh tokens
- **Features**: Employee CRUD, attendance (mark/view/filter), dashboard summary, pagination, generic API/error responses

## Repository structure

```
balkrishna-project/
├── docker-compose.yml    # Postgres + optional backend + frontend
├── backend-hrm/           # FastAPI app (Poetry)
├── frontend-hrm/          # Next.js app (pnpm)
└── README.md
```

## Quick start (local)

### 1. Start Postgres

```bash
docker compose up -d postgres
```

### 2. Backend

```bash
cd backend-hrm
poetry install
cp .env.example .env
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  
- Default admin: `admin@hrms.local` / `admin123`

### 3. Frontend

```bash
cd frontend-hrm
pnpm install
pnpm dev
```

- App: http://localhost:3000  
- Log in with the default admin credentials above.

## Run with Docker (full stack)

```bash
docker compose up -d
```

- Frontend: http://localhost:3000  
- Backend: http://localhost:8000  
- Postgres: localhost:5432 (user `hrms_user`, db `hrms_db`)

## Tech stack

| Layer    | Stack |
|----------|--------|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind 4, Shadcn UI, next-themes |
| Backend  | FastAPI, SQLAlchemy 2 (async), PostgreSQL (asyncpg), Pydantic |
| Auth     | JWT (access + refresh), bcrypt |
| DB       | PostgreSQL 16 |

## Default admin (seeded by backend)

For development and demo, use:

- **Email**: `admin@hrms.local`
- **Password**: `admin123`

The frontend login page shows this so new users can sign in without separate setup.

## Assumptions / limitations

- Single admin user is seeded on first run; no sign-up flow.
- Leave management, payroll, and advanced HR features are out of scope.
- Redis was not used (as requested).

See `backend-hrm/README.md` and `frontend-hrm/README.md` for detailed setup and API/folder structure.
