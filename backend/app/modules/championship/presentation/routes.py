"""HTTP endpoints for current champion and succession history."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.session import get_session
from app.modules.accounts.presentation.dependencies import get_current_user
from app.modules.championship.application.championship_service import (
    get_champion_history,
    get_current_champion,
)
from app.modules.championship.presentation.schemas import ChampionHistoryResponse

router = APIRouter(prefix="/champions", tags=["champions"])


@router.get("/current", response_model=ChampionHistoryResponse | None)
async def read_current_champion(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> ChampionHistoryResponse | None:
    champion = await get_current_champion(session)
    return ChampionHistoryResponse.from_view(champion) if champion else None


@router.get("/history", response_model=list[ChampionHistoryResponse])
async def read_champion_history(
    limit: int = Query(default=100, ge=1, le=500),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[ChampionHistoryResponse]:
    history = await get_champion_history(session, limit=limit)
    return [ChampionHistoryResponse.from_view(entry) for entry in history]
