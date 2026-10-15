"""Dependencies for constructing run and draft application services."""

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.modules.runs.application.draft_service import DraftService
from app.modules.runs.domain.draft_policy import DraftProbabilityPolicy
from app.modules.runs.application.policy_provider import (
    DraftProbabilityConfigurationError,
    get_draft_probability_policy,
)


def get_configured_draft_policy() -> DraftProbabilityPolicy:
    try:
        return get_draft_probability_policy()
    except DraftProbabilityConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


def get_configured_draft_service(
    session: AsyncSession = Depends(get_session),
    policy: DraftProbabilityPolicy = Depends(get_configured_draft_policy),
) -> DraftService:
    return DraftService(session, policy)
