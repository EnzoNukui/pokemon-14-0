from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from types import MappingProxyType

from app.modules.runs.domain.rules import LEGENDARY_OFFER_PROBABILITY

DRAFT_TIERS = frozenset({1, 2, 3, 4, 5})


@dataclass(frozen=True, slots=True)
class DraftProbabilityPolicy:
    """Probabilities for non-legendary tiers; legendary chance is already agreed."""

    tier_weights: Mapping[int, Decimal]

    def __post_init__(self) -> None:
        object.__setattr__(self, "tier_weights", MappingProxyType(dict(self.tier_weights)))
        if set(self.tier_weights) != DRAFT_TIERS:
            raise ValueError("tier_weights must define tiers 1 through 5")
        if any(
            not isinstance(weight, Decimal) or not weight.is_finite()
            for weight in self.tier_weights.values()
        ):
            raise ValueError("tier weights must be finite Decimal values")
        if any(weight < 0 for weight in self.tier_weights.values()):
            raise ValueError("tier weights cannot be negative")
        expected_total = Decimal("1") - LEGENDARY_OFFER_PROBABILITY
        if sum(self.tier_weights.values(), Decimal("0")) != expected_total:
            raise ValueError(
                "tier weights must total 0.99 because legendary offers have 1% probability"
            )
