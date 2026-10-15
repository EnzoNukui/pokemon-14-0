"""HTTP endpoints for run draft generation and selection."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.db.models.user import User
from app.modules.accounts.presentation.dependencies import get_current_user
from app.modules.runs.application.draft_service import (
    DraftCompleted,
    DraftError,
    DraftPoolConfigurationError,
    DraftService,
    DraftUnavailable,
    InvalidDraftSelection,
    RerollUnavailable,
    RunNotFound,
)
from app.modules.runs.presentation.dependencies import get_configured_draft_service
from app.modules.runs.presentation.draft_schemas import (
    DraftRoundResponse,
    DraftSelectionResponse,
    SelectDraftOptionRequest,
)

router = APIRouter(prefix="/runs", tags=["runs and draft"])


def _raise_draft_http_error(error: DraftError) -> None:
    if isinstance(error, RunNotFound):
        raise HTTPException(status_code=404, detail=str(error)) from error
    if isinstance(error, DraftPoolConfigurationError):
        raise HTTPException(status_code=503, detail=str(error)) from error
    if isinstance(error, (DraftUnavailable, DraftCompleted, RerollUnavailable)):
        raise HTTPException(status_code=409, detail=str(error)) from error
    if isinstance(error, InvalidDraftSelection):
        raise HTTPException(status_code=422, detail=str(error)) from error
    raise HTTPException(status_code=400, detail="Draft request could not be completed.") from error


@router.get("/{run_id}/draft", response_model=DraftRoundResponse)
async def read_draft_round(
    run_id: UUID,
    user: User = Depends(get_current_user),
    service: DraftService = Depends(get_configured_draft_service),
) -> DraftRoundResponse:
    try:
        result = await service.get_current_round(user_id=user.id, run_id=run_id)
    except DraftError as exc:
        _raise_draft_http_error(exc)
    return DraftRoundResponse.from_view(result)


@router.post("/{run_id}/draft/reroll", response_model=DraftRoundResponse)
async def reroll_draft_round(
    run_id: UUID,
    user: User = Depends(get_current_user),
    service: DraftService = Depends(get_configured_draft_service),
) -> DraftRoundResponse:
    try:
        result = await service.reroll_current_round(user_id=user.id, run_id=run_id)
    except DraftError as exc:
        _raise_draft_http_error(exc)
    return DraftRoundResponse.from_view(result)


@router.post("/{run_id}/draft/selection", response_model=DraftSelectionResponse)
async def choose_draft_option(
    run_id: UUID,
    payload: SelectDraftOptionRequest,
    user: User = Depends(get_current_user),
    service: DraftService = Depends(get_configured_draft_service),
) -> DraftSelectionResponse:
    try:
        result = await service.select_option(
            user_id=user.id,
            run_id=run_id,
            option_number=payload.option_number,
        )
    except DraftError as exc:
        _raise_draft_http_error(exc)
    return DraftSelectionResponse.from_view(result)
