from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session

router = APIRouter()


@router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Report whether the API process is responding."""
    return {"status": "ok"}


@router.get("/ready", tags=["health"])
async def readiness_check(
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    """Report whether the API can reach its database."""
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail={"status": "not_ready", "database": "unavailable"},
        ) from exc

    return {"status": "ready", "database": "ok"}
