"""Health check API (unauthenticated)."""
from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.db.base import get_db

router = APIRouter()


@router.get("")
async def health(db=Depends(get_db)):
    """Health check: app + database connectivity."""
    try:
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
    return {
        "status": "ok",
        "database": db_status,
    }
