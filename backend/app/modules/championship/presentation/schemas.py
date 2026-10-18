"""HTTP schemas for the current champion and succession history."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.modules.championship.application.championship_service import ChampionHistoryView
from app.modules.championship.application.championship_service import (
    ChampionRankingEntryView,
    ChampionRankingPokemonView,
)


class ChampionHistoryResponse(BaseModel):
    id: UUID
    user_id: UUID | None
    team_id: UUID | None
    trainer_team_id: UUID | None
    run_id: UUID | None
    became_champion_at: datetime
    lost_championship_at: datetime | None

    @classmethod
    def from_view(cls, view: ChampionHistoryView) -> "ChampionHistoryResponse":
        return cls(
            id=view.id,
            user_id=view.user_id,
            team_id=view.team_id,
            trainer_team_id=view.trainer_team_id,
            run_id=view.run_id,
            became_champion_at=view.became_champion_at,
            lost_championship_at=view.lost_championship_at,
        )


class ChampionRankingPokemonResponse(BaseModel):
    pokemon_id: UUID
    pokemon_name: str
    front_sprite_url: str | None
    national_dex_number: int | None

    @classmethod
    def from_view(
        cls, view: ChampionRankingPokemonView
    ) -> "ChampionRankingPokemonResponse":
        return cls(
            pokemon_id=view.pokemon_id,
            pokemon_name=view.pokemon_name,
            front_sprite_url=view.front_sprite_url,
            national_dex_number=view.national_dex_number,
        )


class ChampionRankingEntryResponse(BaseModel):
    id: UUID
    trainer_name: str
    completed_battles: int
    completed_at: datetime
    team: list[ChampionRankingPokemonResponse]

    @classmethod
    def from_view(
        cls, view: ChampionRankingEntryView
    ) -> "ChampionRankingEntryResponse":
        return cls(
            id=view.id,
            trainer_name=view.trainer_name,
            completed_battles=view.completed_battles,
            completed_at=view.completed_at,
            team=[ChampionRankingPokemonResponse.from_view(member) for member in view.team],
        )
