"""HTTP endpoints for battle-path progression within a run."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.modules.battles.application.errors import BattleEngineUnavailable
from app.modules.runs.application.battle_errors import (
    BattleOrderConflict,
    BattlePathConfigurationError,
    BattleProgressionError,
    BattleProgressionUnavailable,
    BattleRunNotFound,
)
from app.modules.runs.application.battle_progression_service import BattleProgressionService
from app.modules.runs.domain.ownership import RunOwner
from app.modules.runs.presentation.ownership import require_run_owner
from app.modules.runs.presentation.battle_schemas import (
    BattleChoiceRequest,
    BattlePathResponse,
    BattleResponse,
    BattleTurnResponse,
)

router = APIRouter(prefix="/runs", tags=["runs and draft"])


def _raise_battle_http_error(error: Exception) -> None:
    if isinstance(error, BattleRunNotFound):
        raise HTTPException(status_code=404, detail=str(error)) from error
    if isinstance(error, (BattlePathConfigurationError, BattleEngineUnavailable)):
        raise HTTPException(status_code=503, detail=str(error)) from error
    if isinstance(error, (BattleProgressionUnavailable, BattleOrderConflict)):
        raise HTTPException(status_code=409, detail=str(error)) from error
    raise HTTPException(
        status_code=400,
        detail="Battle progression could not be completed.",
    ) from error


@router.get("/{run_id}/battles", response_model=BattlePathResponse)
async def read_battle_path(
    run_id: UUID,
    owner: RunOwner = Depends(require_run_owner),
    session: AsyncSession = Depends(get_session),
) -> BattlePathResponse:
    service = BattleProgressionService(session)
    try:
        path = await service.get_path(owner=owner, run_id=run_id)
    except BattleProgressionError as exc:
        _raise_battle_http_error(exc)
    return BattlePathResponse.from_view(path)


@router.get("/{run_id}/battles/current", response_model=BattleResponse)
async def read_current_battle(
    run_id: UUID,
    owner: RunOwner = Depends(require_run_owner),
    session: AsyncSession = Depends(get_session),
) -> BattleResponse:
    service = BattleProgressionService(session)
    try:
        battle = await service.get_current_battle(owner=owner, run_id=run_id)
    except BattleProgressionError as exc:
        _raise_battle_http_error(exc)
    return BattleResponse.from_view(battle)



@router.post("/{run_id}/battles/current/start", response_model=BattleTurnResponse)
async def start_current_battle(
    run_id: UUID,
    owner: RunOwner = Depends(require_run_owner),
    session: AsyncSession = Depends(get_session),
) -> BattleTurnResponse:
    service = BattleProgressionService(session)
    try:
        result = await service.start_current_battle(owner=owner, run_id=run_id)
    except (BattleProgressionError, BattleEngineUnavailable) as exc:
        _raise_battle_http_error(exc)
    return BattleTurnResponse.from_view(result)


@router.post(
    "/{run_id}/battles/{battle_number}/choices",
    response_model=BattleTurnResponse,
)
async def submit_battle_choice(
    run_id: UUID,
    battle_number: int,
    payload: BattleChoiceRequest,
    owner: RunOwner = Depends(require_run_owner),
    session: AsyncSession = Depends(get_session),
) -> BattleTurnResponse:
    service = BattleProgressionService(session)
    try:
        result = await service.submit_battle_choice(
            owner=owner,
            run_id=run_id,
            battle_number=battle_number,
            choice=payload.choice,
        )
    except (BattleProgressionError, BattleEngineUnavailable) as exc:
        _raise_battle_http_error(exc)
    return BattleTurnResponse.from_view(result)
