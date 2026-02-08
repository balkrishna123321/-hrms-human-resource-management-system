# Contributing to HRMS Lite Backend

Thank you for your interest in contributing. This document provides guidelines and setup steps.

## Development setup

1. **Prerequisites**: Python 3.11+, Poetry, PostgreSQL (or use Docker for Postgres only).

2. **Clone and install**:
   ```bash
   cd backend-hrm
   poetry install
   cp .env.example .env
   ```

3. **Start Postgres** (from repo root):
   ```bash
   docker compose up -d postgres
   ```

4. **Run the API**:
   ```bash
   poetry run uvicorn app.main:app --reload --port 8000
   ```
   Or use the Makefile: `make run`.

## Project structure

- `app/main.py` – FastAPI app, lifespan, CORS, exception handlers.
- `app/core/` – Config, security (JWT), dependencies.
- `app/api/v1/` – Route modules: auth, employees, departments, attendance, dashboard, health, reports.
- `app/models/` – SQLAlchemy models.
- `app/schemas/` – Pydantic request/response schemas.
- `app/repositories/` – Data access layer.
- `app/services/` – Business logic.
- `app/db/` – Engine, session, seed.
- `app/utils/` – Generic responses, exceptions.

## Code style

- Use **Ruff** and **Black** for linting/formatting:
  ```bash
  poetry run ruff check app/
  poetry run black app/
  ```
- Type hints are encouraged for public functions and request/response models.

## Testing

- Run tests with pytest:
  ```bash
  poetry run pytest -v
  ```

## API design

- RESTful conventions; JSON request/response.
- Use generic `APIResponse[T]` and `PaginatedResponse[T]` for consistency.
- Errors use `APIErrorResponse` with appropriate HTTP status and `error_code`.

## Default credentials

For local development and demo, a default admin is seeded:

- **Email**: `admin@hrms.local`
- **Password**: `admin123`

Do not use these in production; set a strong password or disable seed.
