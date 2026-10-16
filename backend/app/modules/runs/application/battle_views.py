"""Application views returned by run and battle use cases."""

from dataclasses import dataclass
from uuid import UUID

from app.modules.battles.application.views import BattleEventView


@dataclass(frozen=True, slots=True)
class OpponentPokemonView:
    slot_number: int
    pokemon_id: UUID
    name: str
    form_name: str | None
    primary_type: str
    secondary_type: str | None
    front_sprite_url: str | None
    national_dex_number: int | None
    nature: str
    ability: str
    held_item: str | None
    moves: list[str]
    evs: dict[str, int]
    ivs: dict[str, int]


@dataclass(frozen=True, slots=True)
class BattleView:
    id: UUID
    battle_number: int
    stage: str
    status: str
    trainer_id: UUID
    trainer_name: str
    trainer_sprite_url: str | None
    trainer_team_id: UUID
    team_key: str
    team_category: str
    simulator_result: str | None
    run_result: str | None
    request_snapshot: dict[str, object] | None
    opponent_team: tuple[OpponentPokemonView, ...]


@dataclass(frozen=True, slots=True)
class BattlePathView:
    run_id: UUID
    run_status: str
    run_stage: str
    progress_index: int
    current_battle_number: int | None
    battles: tuple[BattleView, ...]


@dataclass(frozen=True, slots=True)
class BattleTurnView:
    battle_id: UUID
    battle_number: int
    status: str
    request: dict[str, object] | None
    choice_error: str | None
    events: tuple[BattleEventView, ...]
    simulator_result: str | None
    run_result: str | None
    run_status: str
    run_stage: str
    progress_index: int
    next_battle_number: int | None
