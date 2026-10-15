"""Application views for transient Showdown events."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BattleEventView:
    event_type: str
    payload: dict[str, object]
