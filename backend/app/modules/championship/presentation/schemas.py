"""HTTP schemas for the current champion and succession history."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.modules.championship.application.championship_service import ChampionHistoryView


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
