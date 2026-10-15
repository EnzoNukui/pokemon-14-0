"""HTTP schemas for run lifecycle and final results."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.modules.championship.presentation.schemas import ChampionHistoryResponse
from app.modules.runs.application.run_service import (
    RunOutcomeView,
    RunView,
    TeamMemberView,
)


class RunResponse(BaseModel):
    id: UUID
    status: str
    stage: str
    progress_index: int
    reroll_used: bool
    legendary_selected: bool
    created_at: datetime
    ended_at: datetime | None

    @classmethod
    def from_view(cls, view: RunView) -> "RunResponse":
        return cls(
            id=view.id,
            status=view.status,
            stage=view.stage,
            progress_index=view.progress_index,
            reroll_used=view.reroll_used,
            legendary_selected=view.legendary_selected,
            created_at=view.created_at,
            ended_at=view.ended_at,
        )


class RunOutcomeResponse(BaseModel):
    run: RunResponse
    hall_of_fame_snapshot: dict[str, object] | None
    champion_history: ChampionHistoryResponse | None

    @classmethod
    def from_view(cls, view: RunOutcomeView) -> "RunOutcomeResponse":
        return cls(
            run=RunResponse.from_view(view.run),
            hall_of_fame_snapshot=view.hall_of_fame_snapshot,
            champion_history=ChampionHistoryResponse.from_view(view.champion_history)
            if view.champion_history
            else None,
        )


class TeamMemberResponse(BaseModel):
    slot_number: int
    pokemon_id: UUID
    pokemon_name: str
    primary_type: str
    secondary_type: str | None
    build_snapshot: dict[str, object]

    @classmethod
    def from_view(cls, view: TeamMemberView) -> "TeamMemberResponse":
        return cls(
            slot_number=view.slot_number,
            pokemon_id=view.pokemon_id,
            pokemon_name=view.pokemon_name,
            primary_type=view.primary_type,
            secondary_type=view.secondary_type,
            build_snapshot=view.build_snapshot,
        )
