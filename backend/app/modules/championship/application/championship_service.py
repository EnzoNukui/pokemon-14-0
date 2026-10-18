"""Record completed runs and serve the champion succession history."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.battle import Battle
from app.db.models.champion import ChampionHistory, CurrentChampion, HallOfFame
from app.db.models.pokemon import Pokemon
from app.db.models.run import Run
from app.db.models.team import Team, TeamPokemon
from app.db.models.user import User


class ChampionshipConfigurationError(Exception):
    """The run cannot be recorded in championship history as configured."""


@dataclass(frozen=True, slots=True)
class ChampionHistoryView:
    id: UUID
    user_id: UUID | None
    team_id: UUID | None
    trainer_team_id: UUID | None
    run_id: UUID | None
    became_champion_at: datetime
    lost_championship_at: datetime | None


@dataclass(frozen=True, slots=True)
class ChampionRankingPokemonView:
    pokemon_id: UUID
    pokemon_name: str
    front_sprite_url: str | None
    national_dex_number: int | None


@dataclass(frozen=True, slots=True)
class ChampionRankingEntryView:
    id: UUID
    trainer_name: str
    completed_battles: int
    completed_at: datetime
    team: tuple[ChampionRankingPokemonView, ...]


def _to_history_view(entry: ChampionHistory) -> ChampionHistoryView:
    return ChampionHistoryView(
        id=entry.id,
        user_id=entry.user_id,
        team_id=entry.team_id,
        trainer_team_id=entry.trainer_team_id,
        run_id=entry.run_id,
        became_champion_at=entry.became_champion_at,
        lost_championship_at=entry.lost_championship_at,
    )


async def record_run_completion(
    session: AsyncSession, *, run: Run, completed_at: datetime
) -> None:
    """Save the run snapshot and atomically promote its team to champion."""
    team = await session.scalar(
        select(Team).where(Team.run_id == run.id).with_for_update()
    )
    if team is None:
        raise ChampionshipConfigurationError("The completed run has no saved team.")

    team_rows = await session.execute(
        select(TeamPokemon, Pokemon)
        .join(Pokemon, Pokemon.id == TeamPokemon.pokemon_id)
        .where(TeamPokemon.team_id == team.id)
        .order_by(TeamPokemon.slot_number)
    )
    team_snapshot = [
        {
            "slot_number": member.slot_number,
            "pokemon_id": str(pokemon.id),
            "pokemon_name": pokemon.name,
            "form_name": pokemon.form_name,
            "build": member.build_snapshot,
        }
        for member, pokemon in team_rows.all()
    ]
    if len(team_snapshot) != 6:
        raise ChampionshipConfigurationError(
            "The completed run team must contain exactly six Pokémon."
        )

    battle_rows = await session.scalars(
        select(Battle).where(Battle.run_id == run.id).order_by(Battle.battle_number)
    )
    battles_snapshot = [
        {
            "battle_number": item.battle_number,
            "stage": item.stage,
            "trainer_team_id": str(item.trainer_team_id),
            "simulator_result": item.simulator_result,
            "run_result": item.run_result,
        }
        for item in battle_rows.all()
    ]
    performance_snapshot: dict[str, Any] = {
        "run_id": str(run.id),
        "completed_battles": run.progress_index,
        "started_at": run.created_at.isoformat(),
        "completed_at": completed_at.isoformat(),
        "team": team_snapshot,
        "battles": battles_snapshot,
    }
    session.add(
        HallOfFame(
            run_id=run.id,
            user_id=run.user_id,
            team_id=team.id,
            completed_at=completed_at,
            performance_snapshot=performance_snapshot,
        )
    )

    # Serialize simultaneous first-time champions when the singleton is absent.
    await session.execute(text("SELECT pg_advisory_xact_lock(130013001)"))
    current = await session.scalar(
        select(CurrentChampion)
        .where(CurrentChampion.singleton_id == 1)
        .with_for_update()
    )
    if current is not None:
        previous = await session.scalar(
            select(ChampionHistory)
            .where(ChampionHistory.id == current.champion_history_id)
            .with_for_update()
        )
        if previous is not None and previous.lost_championship_at is None:
            previous.lost_championship_at = completed_at

    new_history = ChampionHistory(
        user_id=run.user_id,
        team_id=team.id,
        run_id=run.id,
        became_champion_at=completed_at,
    )
    session.add(new_history)
    await session.flush()
    if current is None:
        session.add(
            CurrentChampion(
                singleton_id=1,
                champion_history_id=new_history.id,
                updated_at=completed_at,
            )
        )
    else:
        current.champion_history_id = new_history.id
        current.updated_at = completed_at


async def get_champion_for_run(
    session: AsyncSession, *, run_id: UUID
) -> ChampionHistoryView | None:
    entry = await session.scalar(
        select(ChampionHistory).where(ChampionHistory.run_id == run_id)
    )
    return _to_history_view(entry) if entry is not None else None


async def get_current_champion(session: AsyncSession) -> ChampionHistoryView | None:
    entry = await session.scalar(
        select(ChampionHistory)
        .join(CurrentChampion, CurrentChampion.champion_history_id == ChampionHistory.id)
        .where(CurrentChampion.singleton_id == 1)
    )
    return _to_history_view(entry) if entry is not None else None


async def get_champion_history(
    session: AsyncSession, *, limit: int = 100
) -> tuple[ChampionHistoryView, ...]:
    rows = await session.scalars(
        select(ChampionHistory)
        .order_by(ChampionHistory.became_champion_at.desc())
        .limit(limit)
    )
    return tuple(_to_history_view(entry) for entry in rows.all())


async def get_champion_ranking(
    session: AsyncSession, *, limit: int = 5
) -> tuple[ChampionRankingEntryView, ...]:
    rows = await session.execute(
        select(HallOfFame, User.trainer_name, Run.progress_index)
        .join(User, User.id == HallOfFame.user_id)
        .join(Run, Run.id == HallOfFame.run_id)
        .order_by(HallOfFame.completed_at.desc())
        .limit(limit)
    )
    champions = rows.all()
    if not champions:
        return ()

    team_ids = [entry.team_id for entry, _, _ in champions]
    team_rows = await session.execute(
        select(
            TeamPokemon.team_id,
            Pokemon.id,
            Pokemon.name,
            Pokemon.front_sprite_url,
            Pokemon.national_dex_number,
        )
        .join(Pokemon, Pokemon.id == TeamPokemon.pokemon_id)
        .where(TeamPokemon.team_id.in_(team_ids))
        .order_by(TeamPokemon.team_id, TeamPokemon.slot_number)
    )
    teams: dict[UUID, list[ChampionRankingPokemonView]] = {}
    for team_id, pokemon_id, name, sprite_url, dex_number in team_rows.all():
        teams.setdefault(team_id, []).append(
            ChampionRankingPokemonView(
                pokemon_id=pokemon_id,
                pokemon_name=name,
                front_sprite_url=sprite_url,
                national_dex_number=dex_number,
            )
        )

    return tuple(
        ChampionRankingEntryView(
            id=entry.id,
            trainer_name=trainer_name,
            completed_battles=completed_battles,
            completed_at=entry.completed_at,
            team=tuple(teams.get(entry.team_id, ())),
        )
        for entry, trainer_name, completed_battles in champions
    )


async def get_run_hall_of_fame_snapshot(
    session: AsyncSession, *, run_id: UUID
) -> dict[str, object] | None:
    entry = await session.scalar(
        select(HallOfFame).where(HallOfFame.run_id == run_id)
    )
    return entry.performance_snapshot if entry is not None else None
