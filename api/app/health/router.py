from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from app.db.session import async_session_factory

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def liveness():
    return {"status": "alive"}


@router.get("/ready")
async def readiness():
    try:
        async with async_session_factory() as session:
            await session.execute(text("SELECT 1"))
    # N.B. health check should not leak internal errors
    except Exception:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Database unavailable")  # noqa: B904

    return {"status": "ready"}
