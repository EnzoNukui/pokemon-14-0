"""HTTP endpoints for current champion and succession history."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.modules.championship.application.championship_service import (
    get_champion_history,
    get_champion_ranking,
    get_current_champion,
)
from app.modules.championship.presentation.schemas import (
    ChampionHistoryResponse,
    ChampionRankingEntryResponse,
)

router = APIRouter(prefix="/champions", tags=["champions"])


@router.get("/ranking", response_model=list[ChampionRankingEntryResponse])
async def read_champion_ranking(
    limit: int = Query(default=5, ge=1, le=50),
    session: AsyncSession = Depends(get_session),
) -> list[ChampionRankingEntryResponse]:
    champions = await get_champion_ranking(session, limit=limit)
    return [ChampionRankingEntryResponse.from_view(entry) for entry in champions]


@router.get("/current", response_model=ChampionHistoryResponse | None)
async def read_current_champion(
    session: AsyncSession = Depends(get_session),
) -> ChampionHistoryResponse | None:
    champion = await get_current_champion(session)
    return ChampionHistoryResponse.from_view(champion) if champion else None


@router.get("/history", response_model=list[ChampionHistoryResponse])
async def read_champion_history(
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_session),
) -> list[ChampionHistoryResponse]:
    history = await get_champion_history(session, limit=limit)
    return [ChampionHistoryResponse.from_view(entry) for entry in history]
