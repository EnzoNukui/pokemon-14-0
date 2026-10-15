"""Load and validate draft tier probabilities from environment settings."""

from decimal import Decimal

from app.core.config import Settings, get_settings
from app.modules.runs.domain.draft_policy import DraftProbabilityPolicy


class DraftProbabilityConfigurationError(Exception):
    """The five tier percentages are missing or do not total 95%."""


def get_draft_probability_policy(
    settings: Settings | None = None,
) -> DraftProbabilityPolicy:
    settings = settings or get_settings()
    configured = {
        1: settings.draft_tier_1_percent,
        2: settings.draft_tier_2_percent,
        3: settings.draft_tier_3_percent,
        4: settings.draft_tier_4_percent,
        5: settings.draft_tier_5_percent,
    }
    if any(value is None for value in configured.values()):
        raise DraftProbabilityConfigurationError(
            "Configure DRAFT_TIER_1_PERCENT through DRAFT_TIER_5_PERCENT in .env."
        )
    weights = {
        tier: value / Decimal("100")
        for tier, value in configured.items()
        if value is not None
    }
    try:
        return DraftProbabilityPolicy(tier_weights=weights)
    except ValueError as exc:
        raise DraftProbabilityConfigurationError(
            "Draft tier percentages must be non-negative and total 95%."
        ) from exc
