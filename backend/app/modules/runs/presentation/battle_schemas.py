"""HTTP schemas for run battle paths, turns, and event history."""

from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.battles.application.views import BattleEventView
from app.modules.battles.domain.outcomes import SimulatorResult
from app.modules.runs.application.battle_views import (
    BattlePathView,
    BattleTurnView,
    BattleView,
    OpponentPokemonView,
)


class BattlePokemonResponse(BaseModel):
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

    @classmethod
    def from_view(cls, view: OpponentPokemonView) -> "BattlePokemonResponse":
        return cls(
            slot_number=view.slot_number,
            pokemon_id=view.pokemon_id,
            name=view.name,
            form_name=view.form_name,
            primary_type=view.primary_type,
            secondary_type=view.secondary_type,
            front_sprite_url=view.front_sprite_url,
            national_dex_number=view.national_dex_number,
            nature=view.nature,
            ability=view.ability,
            held_item=view.held_item,
            moves=view.moves,
            evs=view.evs,
            ivs=view.ivs,
        )


class BattleResponse(BaseModel):
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
    opponent_team: list[BattlePokemonResponse]

    @classmethod
    def from_view(cls, view: BattleView) -> "BattleResponse":
        return cls(
            id=view.id,
            battle_number=view.battle_number,
            stage=view.stage,
            status=view.status,
            trainer_id=view.trainer_id,
            trainer_name=view.trainer_name,
            trainer_sprite_url=view.trainer_sprite_url,
            trainer_team_id=view.trainer_team_id,
            team_key=view.team_key,
            team_category=view.team_category,
            simulator_result=view.simulator_result,
            run_result=view.run_result,
            request_snapshot=view.request_snapshot,
            opponent_team=[BattlePokemonResponse.from_view(pokemon) for pokemon in view.opponent_team],
        )


class BattlePathResponse(BaseModel):
    run_id: UUID
    run_status: str
    run_stage: str
    progress_index: int
    current_battle_number: int | None
    battles: list[BattleResponse]

    @classmethod
    def from_view(cls, view: BattlePathView) -> "BattlePathResponse":
        return cls(
            run_id=view.run_id,
            run_status=view.run_status,
            run_stage=view.run_stage,
            progress_index=view.progress_index,
            current_battle_number=view.current_battle_number,
            battles=[BattleResponse.from_view(battle) for battle in view.battles],
        )


class BattleChoiceRequest(BaseModel):
    choice: str = Field(min_length=1, max_length=40)


class BattleProtocolEventResponse(BaseModel):
    event_type: str
    payload: dict[str, object]

    @classmethod
    def from_view(cls, view: BattleEventView) -> "BattleProtocolEventResponse":
        return cls(
            event_type=view.event_type,
            payload=view.payload,
        )


class BattleTurnResponse(BaseModel):
    battle_id: UUID
    battle_number: int
    status: str
    request: dict[str, object] | None
    choice_error: str | None
    events: list[BattleProtocolEventResponse]
    simulator_result: SimulatorResult | None
    run_result: str | None
    run_status: str
    run_stage: str
    progress_index: int
    next_battle_number: int | None

    @classmethod
    def from_view(cls, view: BattleTurnView) -> "BattleTurnResponse":
        return cls(
            battle_id=view.battle_id,
            battle_number=view.battle_number,
            status=view.status,
            request=view.request,
            choice_error=view.choice_error,
            events=[BattleProtocolEventResponse.from_view(event) for event in view.events],
            simulator_result=SimulatorResult(view.simulator_result)
            if view.simulator_result
            else None,
            run_result=view.run_result,
            run_status=view.run_status,
            run_stage=view.run_stage,
            progress_index=view.progress_index,
            next_battle_number=view.next_battle_number,
        )
