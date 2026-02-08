"""FastAPI application entrypoint."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.v1.router import api_router
from app.db.base import engine, Base, AsyncSessionLocal
from app.db.seed import (
    seed_admin,
    seed_departments,
    seed_permissions,
    seed_roles,
    seed_leave_types,
    seed_holidays,
    seed_fill_permissions,
    seed_fill_roles,
    seed_fill_departments,
    seed_fill_leave_types,
    seed_fill_holidays,
    seed_employees_dummy,
    seed_leave_balances_dummy,
    seed_leave_requests_dummy,
    seed_attendance_dummy,
)
from app.utils.exceptions import AppException, app_exception_handler, validation_exception_handler
from fastapi.exceptions import RequestValidationError

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup and seed default admin (dev)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        await seed_permissions(session)
        await seed_roles(session)
        await seed_admin(session)
        await seed_departments(session)
        await seed_leave_types(session)
        await seed_holidays(session)
        await seed_fill_permissions(session)
        await seed_fill_roles(session)
        await seed_fill_departments(session)
        await seed_fill_leave_types(session)
        await seed_fill_holidays(session)
        await seed_employees_dummy(session)
        await seed_leave_balances_dummy(session)
        await seed_leave_requests_dummy(session)
        await seed_attendance_dummy(session)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="HRMS Lite - Employee and Attendance Management API",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok", "service": settings.APP_NAME}
