"""Use cases for starting, viewing and abandoning a user's run."""

from dataclasses import dataclass
from datetime import datetime, timezone
from secrets import randbits
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.pokemon import Pokemon
from app.db.models.battle import Battle
from app.db.models.run import Run
from app.db.models.team import Team, TeamPokemon
from app.modules.battles.application.battle_service import BattleService
from app.modules.championship.application.championship_service import (
    ChampionHistoryView,
    get_champion_for_run,
    get_run_hall_of_fame_snapshot,
)
from app.modules.runs.domain.states import RunStage, RunStatus


class ActiveRunAlreadyExists(Exception):
    """The account already has an active run."""


class RunDoesNotExist(Exception):
    """No run belonging to the account matches the request."""


@dataclass(frozen=True, slots=True)
class RunView:
    id: UUID
    status: str
    stage: str
    progress_index: int
    reroll_used: bool
    legendary_selected: bool
    created_at: datetime
    ended_at: datetime | None


@dataclass(frozen=True, slots=True)
class RunOutcomeView:
    run: RunView
    hall_of_fame_snapshot: dict[str, object] | None
    champion_history: ChampionHistoryView | None


@dataclass(frozen=True, slots=True)
class TeamMemberView:
    slot_number: int
    pokemon_id: UUID
    pokemon_name: str
    primary_type: str
    secondary_type: str | None
    build_snapshot: dict[str, object]


def to_run_view(run: Run) -> RunView:
    return RunView(
        id=run.id,
        status=run.status,
        stage=run.stage,
        progress_index=run.progress_index,
        reroll_used=run.reroll_used,
        legendary_selected=run.legendary_selected,
        created_at=run.created_at,
        ended_at=run.ended_at,
    )


async def create_run(session: AsyncSession, *, user_id: UUID) -> RunView:
    existing = await session.scalar(
        select(Run.id).where(
            Run.user_id == user_id,
            Run.status == RunStatus.ACTIVE.value,
        )
    )
    if existing is not None:
        raise ActiveRunAlreadyExists

    run = Run(
        user_id=user_id,
        status=RunStatus.ACTIVE.value,
        stage=RunStage.DRAFT.value,
        progress_index=0,
        random_seed=randbits(63),
    )
    session.add(run)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        # The partial unique index is the final guard against concurrent starts.
        raise ActiveRunAlreadyExists from exc
    await session.refresh(run)
    return to_run_view(run)


async def get_current_run(session: AsyncSession, *, user_id: UUID) -> RunView:
    run = await session.scalar(
        select(Run)
        .where(Run.user_id == user_id, Run.status == RunStatus.ACTIVE.value)
        .order_by(Run.created_at.desc())
    )
    if run is None:
        raise RunDoesNotExist
    return to_run_view(run)


async def get_run_history(
    session: AsyncSession, *, user_id: UUID, limit: int = 100
) -> tuple[RunView, ...]:
    rows = await session.scalars(
        select(Run)
        .where(
            Run.user_id == user_id,
            Run.status.in_(
                (
                    RunStatus.FAILED.value,
                    RunStatus.COMPLETED.value,
                    RunStatus.ABANDONED.value,
                )
            ),
        )
        .order_by(Run.ended_at.desc(), Run.created_at.desc())
        .limit(limit)
    )
    return tuple(to_run_view(run) for run in rows.all())


async def get_run_outcome(
    session: AsyncSession, *, user_id: UUID, run_id: UUID
) -> RunOutcomeView:
    run = await session.scalar(
        select(Run).where(Run.id == run_id, Run.user_id == user_id)
    )
    if run is None:
        raise RunDoesNotExist
    return RunOutcomeView(
        run=to_run_view(run),
        hall_of_fame_snapshot=await get_run_hall_of_fame_snapshot(
            session, run_id=run.id
        ),
        champion_history=await get_champion_for_run(session, run_id=run.id),
    )


async def abandon_run(
    session: AsyncSession, *, user_id: UUID, run_id: UUID
) -> RunView:
    run = await session.scalar(
        select(Run)
        .where(
            Run.id == run_id,
            Run.user_id == user_id,
            Run.status == RunStatus.ACTIVE.value,
        )
        .with_for_update()
    )
    if run is None:
        raise RunDoesNotExist
    battle = await session.scalar(
        select(Battle)
        .where(Battle.run_id == run.id, Battle.status == "RUNNING")
        .with_for_update()
    )
    now = datetime.now(timezone.utc)
    if battle is not None:
        await BattleService(session).abandon(battle, finished_at=now)
    run.status = RunStatus.ABANDONED.value
    run.ended_at = now
    run.version += 1
    await session.commit()
    return to_run_view(run)


async def get_run_team(
    session: AsyncSession, *, user_id: UUID, run_id: UUID
) -> tuple[TeamMemberView, ...]:
    owned_run = await session.scalar(
        select(Run.id).where(Run.id == run_id, Run.user_id == user_id)
    )
    if owned_run is None:
        raise RunDoesNotExist

    rows = await session.execute(
        select(TeamPokemon, Pokemon)
        .join(Team, Team.id == TeamPokemon.team_id)
        .join(Pokemon, Pokemon.id == TeamPokemon.pokemon_id)
        .where(Team.run_id == run_id)
        .order_by(TeamPokemon.slot_number)
    )
    return tuple(
        TeamMemberView(
            slot_number=member.slot_number,
            pokemon_id=pokemon.id,
            pokemon_name=pokemon.name,
            primary_type=pokemon.primary_type,
            secondary_type=pokemon.secondary_type,
            build_snapshot=member.build_snapshot,
        )
        for member, pokemon in rows.all()
    )
