"""Manage one Showdown battle and translate its transient events."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.battle import Battle
from app.db.models.pokemon import Pokemon
from app.db.models.team import Team, TeamPokemon
from app.db.models.trainer import Trainer, TrainerTeam, TrainerTeamPokemon
from app.modules.battles.application.errors import (
    BattleEngineResponseError,
    BattleEngineUnavailable,
)
from app.modules.battles.application.views import BattleEventView
from app.modules.battles.infrastructure.showdown_client import (
    ShowdownClient,
    ShowdownUnavailable,
)
from app.modules.battles.infrastructure.team_mapper import to_engine_set


class BattleService:
    """Owns Showdown calls, battle state persistence, and event serialization."""

    def __init__(
        self, session: AsyncSession, showdown: ShowdownClient | None = None
    ) -> None:
        self._session = session
        self._showdown = showdown or ShowdownClient()

    async def resume(self, battle: Battle) -> tuple[dict[str, object], tuple[BattleEventView, ...]]:
        try:
            engine_result = await self._showdown.get_battle(battle_id=battle.id)
        except ShowdownUnavailable as exc:
            raise BattleEngineUnavailable(str(exc)) from exc
        events = self._map_engine_events(engine_result)
        battle.request_snapshot = engine_result.get("request")
        return engine_result, events

    async def start(
        self, *, battle: Battle, run_id: UUID, trainer_team_id: UUID
    ) -> tuple[dict[str, object], tuple[BattleEventView, ...]]:
        player_team = await self._load_player_engine_team(run_id=run_id)
        opponent_name, opponent_team = await self._load_opponent_engine_team(
            trainer_team_id=trainer_team_id
        )
        try:
            engine_result = await self._showdown.start_battle(
                battle_id=battle.id,
                player_name="Player",
                player_team=player_team,
                opponent_name=opponent_name,
                opponent_team=opponent_team,
                battle_format="gen9nationaldexag",
            )
        except ShowdownUnavailable as exc:
            raise BattleEngineUnavailable(str(exc)) from exc

        now = datetime.now(timezone.utc)
        battle.status = "RUNNING"
        battle.battle_format = "gen9nationaldexag"
        battle.engine_version = str(engine_result.get("engine_version", "unknown"))
        battle.request_snapshot = engine_result.get("request")
        battle.started_at = now
        events = self._map_engine_events(engine_result)
        return engine_result, events

    async def submit_choice(
        self, *, battle: Battle, choice: str
    ) -> tuple[dict[str, object], tuple[BattleEventView, ...]]:
        try:
            engine_result = await self._showdown.submit_choice(
                battle_id=battle.id, choice=choice
            )
        except ShowdownUnavailable as exc:
            raise BattleEngineUnavailable(str(exc)) from exc
        events = self._map_engine_events(engine_result)
        battle.request_snapshot = engine_result.get("request")
        return engine_result, events

    async def abandon(self, battle: Battle, *, finished_at: datetime) -> None:
        try:
            await self._showdown.abandon_battle(battle_id=battle.id)
        except ShowdownUnavailable:
            # The run must still be abandonable if the engine is offline.
            pass
        battle.status = "ABANDONED"
        battle.finished_at = finished_at

    async def _load_player_engine_team(self, *, run_id: UUID) -> list[dict[str, object]]:
        rows = await self._session.execute(
            select(TeamPokemon, Pokemon)
            .join(Team, Team.id == TeamPokemon.team_id)
            .join(Pokemon, Pokemon.id == TeamPokemon.pokemon_id)
            .where(Team.run_id == run_id)
            .order_by(TeamPokemon.slot_number)
        )
        members = rows.all()
        if len(members) != 6:
            raise BattleEngineResponseError(
                "The player team must contain exactly six Pokémon before a battle starts."
            )
        return [
            to_engine_set(pokemon.name, pokemon.form_name, member.build_snapshot)
            for member, pokemon in members
        ]

    async def _load_opponent_engine_team(
        self, *, trainer_team_id: UUID
    ) -> tuple[str, list[dict[str, object]]]:
        trainer_name = await self._session.scalar(
            select(Trainer.name)
            .join(TrainerTeam, TrainerTeam.trainer_id == Trainer.id)
            .where(TrainerTeam.id == trainer_team_id)
        )
        rows = await self._session.execute(
            select(TrainerTeamPokemon, Pokemon)
            .join(Pokemon, Pokemon.id == TrainerTeamPokemon.pokemon_id)
            .where(TrainerTeamPokemon.trainer_team_id == trainer_team_id)
            .order_by(TrainerTeamPokemon.slot_number)
        )
        members = rows.all()
        if trainer_name is None or len(members) != 6:
            raise BattleEngineResponseError(
                "The selected trainer must have a complete six-Pokémon team."
            )
        team = [
            to_engine_set(
                pokemon.name,
                pokemon.form_name,
                {
                    "nature": member.nature,
                    "ability": member.ability,
                    "held_item": member.held_item,
                    "moves": member.moves,
                    "evs": member.evs,
                    "ivs": member.ivs,
                },
            )
            for member, pokemon in members
        ]
        return trainer_name, team

    @staticmethod
    def _map_engine_events(
        engine_result: dict[str, object],
    ) -> tuple[BattleEventView, ...]:
        raw_events = engine_result.get("events", [])
        if not isinstance(raw_events, list):
            raise BattleEngineResponseError("Showdown returned malformed battle events.")
        live_events: list[BattleEventView] = []
        for event in raw_events:
            if not isinstance(event, dict):
                continue
            event_type = event.get("event_type")
            payload = event.get("payload")
            if not isinstance(event_type, str) or not isinstance(payload, dict):
                continue
            normalized_payload = {str(key): value for key, value in payload.items()}
            event_type = event_type[:80]
            live_events.append(
                BattleEventView(
                    event_type=event_type,
                    payload=normalized_payload,
                )
            )
        return tuple(live_events)
