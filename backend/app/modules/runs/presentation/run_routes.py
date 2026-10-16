"""HTTP endpoints for starting, reading, and ending runs."""

from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.session import get_session
from app.modules.accounts.presentation.dependencies import get_current_user
from app.modules.runs.application.run_service import (
    ActiveRunAlreadyExists,
    RunNotCompleted,
    RunDoesNotExist,
    abandon_run,
    claim_completed_guest_run,
    create_run,
    get_run_outcome,
    get_run_history,
    get_current_run,
    get_run_team,
)
from app.modules.championship.application.championship_service import (
    ChampionshipConfigurationError,
)
from app.modules.runs.application.guest_sessions import (
    create_guest_session,
    get_guest_session_id,
)
from app.modules.runs.domain.ownership import RunOwner
from app.modules.runs.presentation.ownership import (
    get_optional_run_owner,
    require_run_owner,
)
from app.modules.runs.domain.draft_policy import DraftProbabilityPolicy
from app.modules.runs.presentation.dependencies import get_configured_draft_policy
from app.modules.runs.presentation.run_schemas import (
    RunOutcomeResponse,
    RunResponse,
    StartRunResponse,
    TeamMemberResponse,
)

router = APIRouter(prefix="/runs", tags=["runs and draft"])


@router.post("", response_model=StartRunResponse, status_code=status.HTTP_201_CREATED)
async def start_run(
    owner: RunOwner | None = Depends(get_optional_run_owner),
    session: AsyncSession = Depends(get_session),
    _policy: DraftProbabilityPolicy = Depends(get_configured_draft_policy),
) -> StartRunResponse:
    guest_session_token = None
    if owner is None:
        guest_session, guest_session_token = await create_guest_session(session)
        owner = RunOwner(guest_session_id=guest_session.id)
    try:
        run = await create_run(session, owner=owner)
    except ActiveRunAlreadyExists as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This player already has an active run.",
        ) from exc
    return StartRunResponse.from_view(run, guest_session_token=guest_session_token)


@router.get("/current", response_model=RunResponse)
async def read_current_run(
    owner: RunOwner = Depends(require_run_owner),
    session: AsyncSession = Depends(get_session),
) -> RunResponse:
    try:
        run = await get_current_run(session, owner=owner)
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
    owner: RunOwner = Depends(require_run_owner),
    session: AsyncSession = Depends(get_session),
) -> RunOutcomeResponse:
    try:
        outcome = await get_run_outcome(session, owner=owner, run_id=run_id)
    except RunDoesNotExist as exc:
        raise HTTPException(status_code=404, detail="Run was not found for this account.") from exc
    return RunOutcomeResponse.from_view(outcome)


@router.get("/{run_id}/team", response_model=list[TeamMemberResponse])
async def read_run_team(
    run_id: UUID,
    owner: RunOwner = Depends(require_run_owner),
    session: AsyncSession = Depends(get_session),
) -> list[TeamMemberResponse]:
    try:
        members = await get_run_team(session, owner=owner, run_id=run_id)
    except RunDoesNotExist as exc:
        raise HTTPException(
            status_code=404,
            detail="Run was not found for this account.",
        ) from exc
    return [TeamMemberResponse.from_view(member) for member in members]


@router.post("/{run_id}/abandon", response_model=RunResponse)
async def end_run(
    run_id: UUID,
    owner: RunOwner = Depends(require_run_owner),
    session: AsyncSession = Depends(get_session),
) -> RunResponse:
    try:
        run = await abandon_run(session, owner=owner, run_id=run_id)
    except RunDoesNotExist as exc:
        raise HTTPException(status_code=404, detail="Active run was not found.") from exc
    return RunResponse.from_view(run)


@router.post("/{run_id}/ranking", response_model=RunOutcomeResponse)
async def submit_run_to_ranking(
    run_id: UUID,
    guest_token: str | None = Header(default=None, alias="X-Guest-Session"),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> RunOutcomeResponse:
    if not guest_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The guest session that owns this run is required.",
        )
    guest_session_id = await get_guest_session_id(session, token=guest_token)
    if guest_session_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Guest session is invalid or expired.",
        )
    await session.commit()
    try:
        await claim_completed_guest_run(
            session,
            user_id=user.id,
            guest_session_id=guest_session_id,
            run_id=run_id,
        )
        outcome = await get_run_outcome(
            session, owner=RunOwner(user_id=user.id), run_id=run_id
        )
    except RunDoesNotExist as exc:
        raise HTTPException(status_code=404, detail="Guest run was not found.") from exc
    except RunNotCompleted as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only a completed winning run can be submitted to the ranking.",
        ) from exc
    except ChampionshipConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    return RunOutcomeResponse.from_view(outcome)
