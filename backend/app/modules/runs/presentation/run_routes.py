"""HTTP endpoints for starting, reading, and ending runs."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.session import get_session
from app.modules.accounts.presentation.dependencies import get_current_user
from app.modules.runs.application.run_service import (
    ActiveRunAlreadyExists,
    RunDoesNotExist,
    abandon_run,
    create_run,
    get_run_outcome,
    get_run_history,
    get_current_run,
    get_run_team,
)
from app.modules.runs.domain.draft_policy import DraftProbabilityPolicy
from app.modules.runs.presentation.dependencies import get_configured_draft_policy
from app.modules.runs.presentation.run_schemas import (
    RunOutcomeResponse,
    RunResponse,
    TeamMemberResponse,
)

router = APIRouter(prefix="/runs", tags=["runs and draft"])


@router.post("", response_model=RunResponse, status_code=status.HTTP_201_CREATED)
async def start_run(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    _policy: DraftProbabilityPolicy = Depends(get_configured_draft_policy),
) -> RunResponse:
    try:
        run = await create_run(session, user_id=user.id)
    except ActiveRunAlreadyExists as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This account already has an active run.",
        ) from exc
    return RunResponse.from_view(run)


@router.get("/current", response_model=RunResponse)
async def read_current_run(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> RunResponse:
    try:
        run = await get_current_run(session, user_id=user.id)
    except RunDoesNotExist as exc:
        raise HTTPException(status_code=404, detail="This account has no active run.") from exc
    return RunResponse.from_view(run)


@router.get("/history", response_model=list[RunResponse])
async def read_run_history(
    limit: int = Query(default=100, ge=1, le=500),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[RunResponse]:
    runs = await get_run_history(session, user_id=user.id, limit=limit)
    return [RunResponse.from_view(run) for run in runs]


@router.get("/{run_id}/result", response_model=RunOutcomeResponse)
async def read_run_outcome(
    run_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> RunOutcomeResponse:
    try:
        outcome = await get_run_outcome(session, user_id=user.id, run_id=run_id)
    except RunDoesNotExist as exc:
        raise HTTPException(status_code=404, detail="Run was not found for this account.") from exc
    return RunOutcomeResponse.from_view(outcome)


@router.get("/{run_id}/team", response_model=list[TeamMemberResponse])
async def read_run_team(
    run_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[TeamMemberResponse]:
    try:
        members = await get_run_team(session, user_id=user.id, run_id=run_id)
    except RunDoesNotExist as exc:
        raise HTTPException(
            status_code=404,
            detail="Run was not found for this account.",
        ) from exc
    return [TeamMemberResponse.from_view(member) for member in members]


@router.post("/{run_id}/abandon", response_model=RunResponse)
async def end_run(
    run_id: UUID,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> RunResponse:
    try:
        run = await abandon_run(session, user_id=user.id, run_id=run_id)
    except RunDoesNotExist as exc:
        raise HTTPException(status_code=404, detail="Active run was not found.") from exc
    return RunResponse.from_view(run)
