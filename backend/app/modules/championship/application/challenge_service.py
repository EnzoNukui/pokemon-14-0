"""Simulate a completed player's team against the latest former champion."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.champion import ChampionHistory
from app.db.models.pokemon import Pokemon
from app.db.models.run import Run
from app.db.models.team import Team, TeamPokemon
from app.db.models.user import User
from app.modules.battles.application.errors import BattleEngineUnavailable
from app.modules.battles.infrastructure.showdown_client import (
    ShowdownClient,
    ShowdownUnavailable,
)
from app.modules.battles.infrastructure.team_mapper import to_engine_set
from app.modules.runs.application.ownership import run_owner_condition
from app.modules.runs.domain.ownership import RunOwner


class ChallengeRunNotFound(Exception):
    """The requested completed run does not belong to the caller."""


class ChallengeRunNotCompleted(Exception):
    """Champion challenges are only available after winning a run."""


class NoPreviousChampion(Exception):
    """There is no saved champion team to challenge yet."""


@dataclass(frozen=True, slots=True)
class ChampionPokemon:
    pokemon_id: UUID
    pokemon_name: str
    primary_type: str
    secondary_type: str | None
    front_sprite_url: str | None
    national_dex_number: int | None


@dataclass(frozen=True, slots=True)
class ChampionChallengeResult:
    battle_id: UUID
    simulator_result: str
    champion_name: str
    became_champion_at: datetime
    team: tuple[ChampionPokemon, ...]


async def simulate_champion_challenge(
    session: AsyncSession,
    *,
    owner: RunOwner,
    run_id: UUID,
    showdown: ShowdownClient | None = None,
) -> ChampionChallengeResult:
    run = await session.scalar(
        select(Run).where(Run.id == run_id, run_owner_condition(owner))
    )
    if run is None:
        raise ChallengeRunNotFound
    if run.status != "COMPLETED":
        raise ChallengeRunNotCompleted

    champion_row = (
        await session.execute(
            select(ChampionHistory, User.trainer_name)
            .outerjoin(User, User.id == ChampionHistory.user_id)
            .where(
                ChampionHistory.run_id.is_not(None),
                ChampionHistory.run_id != run_id,
                ChampionHistory.team_id.is_not(None),
            )
            .order_by(ChampionHistory.became_champion_at.desc())
            .limit(1)
        )
    ).first()
    if champion_row is None:
        raise NoPreviousChampion

    champion, champion_name = champion_row
    opponent_name = champion_name or "Campeão anterior"
    current_team_rows = await session.execute(
        select(TeamPokemon, Pokemon)
        .join(Team, Team.id == TeamPokemon.team_id)
        .join(Pokemon, Pokemon.id == TeamPokemon.pokemon_id)
        .where(Team.run_id == run_id)
        .order_by(TeamPokemon.slot_number)
    )
    opponent_team_rows = await session.execute(
        select(TeamPokemon, Pokemon)
        .join(Pokemon, Pokemon.id == TeamPokemon.pokemon_id)
        .where(TeamPokemon.team_id == champion.team_id)
        .order_by(TeamPokemon.slot_number)
    )
    current_members = current_team_rows.all()
    opponent_members = opponent_team_rows.all()
    if len(current_members) != 6 or len(opponent_members) != 6:
        raise NoPreviousChampion

    player_team = [
        to_engine_set(
            pokemon.name,
            pokemon.form_name,
            member.build_snapshot,
            level=65,
        )
        for member, pokemon in current_members
    ]
    opponent_team = [
        to_engine_set(
            pokemon.name,
            pokemon.form_name,
            member.build_snapshot,
            level=65,
        )
        for member, pokemon in opponent_members
    ]
    public_team = tuple(
        ChampionPokemon(
            pokemon_id=pokemon.id,
            pokemon_name=pokemon.name,
            primary_type=pokemon.primary_type,
            secondary_type=pokemon.secondary_type,
            front_sprite_url=pokemon.front_sprite_url,
            national_dex_number=pokemon.national_dex_number,
        )
        for _, pokemon in opponent_members
    )
    await session.commit()
    battle_id = uuid4()
    engine = showdown or ShowdownClient()
    try:
        result = await engine.start_battle(
            battle_id=battle_id,
            player_name=f"Desafiante-{battle_id.hex[:6]}",
            player_team=player_team,
            opponent_name=opponent_name,
            opponent_category="CHAMPION_CHALLENGE",
            opponent_team=opponent_team,
            battle_format="gen9nationaldexag",
        )
    except ShowdownUnavailable as exc:
        raise BattleEngineUnavailable(str(exc)) from exc
    finally:
        try:
            await engine.abandon_battle(battle_id=battle_id)
        except ShowdownUnavailable:
            pass

    outcome = result.get("simulator_result")
    if outcome not in {"WIN", "LOSS", "DRAW"}:
        raise BattleEngineUnavailable("The champion challenge did not return a result.")

    return ChampionChallengeResult(
        battle_id=battle_id,
        simulator_result=str(outcome),
        champion_name=opponent_name,
        became_champion_at=champion.became_champion_at,
        team=public_team,
    )
