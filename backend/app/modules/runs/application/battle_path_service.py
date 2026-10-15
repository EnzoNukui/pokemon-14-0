"""Build and read the fixed sequence of opponents assigned to a run."""

from __future__ import annotations

from hashlib import sha256
from random import Random
from secrets import randbits
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.battle import Battle
from app.db.models.pokemon import Pokemon
from app.db.models.run import Run
from app.db.models.trainer import Trainer, TrainerTeam, TrainerTeamPokemon
from app.modules.runs.application.battle_errors import (
    BattlePathConfigurationError,
    BattleProgressionUnavailable,
    BattleRunNotFound,
)
from app.modules.runs.application.battle_views import (
    BattlePathView,
    BattleView,
    OpponentPokemonView,
)
from app.modules.runs.domain.rules import (
    ELITE_FOUR_BATTLES,
    GYM_BATTLES,
    TOTAL_BATTLES,
    stage_for_battle_number,
)
from app.modules.runs.domain.states import RunStage, RunStatus

class BattlePathService:
    """Owns opponent selection and the persisted 13-battle path."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_path(self, *, user_id: UUID, run_id: UUID) -> BattlePathView:
        async with self._session.begin():
            run = await self.get_owned_run(user_id=user_id, run_id=run_id, lock=True)
            if run.stage == RunStage.DRAFT.value:
                raise BattleProgressionUnavailable(
                    "Finish the six-Pokémon draft before starting the battle path."
                )
            await self.ensure_path(run)
            rows = await self.load_battles(run_id)
            views = await self.to_battle_views(rows)
            next_number = (
                run.progress_index + 1
                if run.status == RunStatus.ACTIVE.value
                and run.progress_index < TOTAL_BATTLES
                else None
            )
            return BattlePathView(
                run_id=run.id,
                run_status=run.status,
                run_stage=run.stage,
                progress_index=run.progress_index,
                current_battle_number=next_number,
                battles=views,
            )

    async def get_current_battle(self, *, user_id: UUID, run_id: UUID) -> BattleView:
        async with self._session.begin():
            run = await self.get_owned_run(user_id=user_id, run_id=run_id, lock=True)
            self.require_active_battle_run(run)
            await self.ensure_path(run)
            battle_number = run.progress_index + 1
            rows = await self.load_battles(run_id, battle_number=battle_number)
            if not rows:
                raise BattlePathConfigurationError(
                    "The next battle is missing from the run path."
                )
            return (await self.to_battle_views(rows))[0]

    async def get_owned_run(self, *, user_id: UUID, run_id: UUID, lock: bool) -> Run:
        statement = select(Run).where(Run.id == run_id, Run.user_id == user_id)
        if lock:
            statement = statement.with_for_update()
        run = await self._session.scalar(statement)
        if run is None:
            raise BattleRunNotFound("Run was not found for this account.")
        return run

    @staticmethod
    def require_active_battle_run(run: Run) -> None:
        if run.status != RunStatus.ACTIVE.value:
            raise BattleProgressionUnavailable("This run is no longer active.")
        if run.stage == RunStage.DRAFT.value:
            raise BattleProgressionUnavailable(
                "Finish the six-Pokémon draft before starting the battle path."
            )
        if run.progress_index >= TOTAL_BATTLES:
            raise BattleProgressionUnavailable("This run has no battles remaining.")

    async def ensure_path(self, run: Run) -> None:
        existing = list(
            (
                await self._session.scalars(
                    select(Battle)
                    .where(Battle.run_id == run.id)
                    .order_by(Battle.battle_number)
                )
            ).all()
        )
        if len(existing) == TOTAL_BATTLES:
            return
        if existing:
            raise BattlePathConfigurationError(
                "The run has a partial battle path; refusing to change its opponents."
            )

        team_rows = await self._session.execute(
            select(TrainerTeam, Trainer)
            .join(Trainer, Trainer.id == TrainerTeam.trainer_id)
            .where(TrainerTeam.is_active.is_(True))
            .order_by(Trainer.id, TrainerTeam.category, TrainerTeam.team_key)
        )
        teams_by_category: dict[str, dict[UUID, list[TrainerTeam]]] = {
            "GYM_LEADER": {},
            "ELITE_FOUR": {},
            "CHAMPION": {},
        }
        for trainer_team, trainer in team_rows.all():
            category = trainer_team.category
            if category in teams_by_category:
                teams_by_category[category].setdefault(trainer.id, []).append(trainer_team)

        if run.random_seed is None:
            run.random_seed = randbits(63)
        seed_material = f"{run.random_seed}:trainer-path:v1".encode("ascii")
        rng = Random(int.from_bytes(sha256(seed_material).digest(), "big"))
        used_trainer_ids: set[UUID] = set()
        scheduled: list[Battle] = []

        for battle_number in range(1, TOTAL_BATTLES + 1):
            eligible_trainers: dict[UUID, list[TrainerTeam]] = {}
            for category in self.eligible_categories(battle_number):
                for trainer_id, variants in teams_by_category[category].items():
                    if trainer_id in used_trainer_ids:
                        continue
                    eligible_trainers.setdefault(trainer_id, []).extend(variants)

            if not eligible_trainers:
                raise BattlePathConfigurationError(
                    f"No unused trainer team is configured for battle {battle_number}."
                )
            trainer_id = rng.choice(list(eligible_trainers))
            trainer_team = rng.choice(eligible_trainers[trainer_id])
            used_trainer_ids.add(trainer_id)
            scheduled.append(
                Battle(
                    run_id=run.id,
                    trainer_team_id=trainer_team.id,
                    battle_number=battle_number,
                    stage=stage_for_battle_number(battle_number).value,
                    status="PENDING",
                )
            )

        self._session.add_all(scheduled)
        await self._session.flush()

    @staticmethod
    def eligible_categories(battle_number: int) -> tuple[str, ...]:
        if battle_number <= GYM_BATTLES:
            return ("GYM_LEADER",)
        if battle_number < GYM_BATTLES + ELITE_FOUR_BATTLES:
            return ("ELITE_FOUR",)
        if battle_number == GYM_BATTLES + ELITE_FOUR_BATTLES:
            return ("ELITE_FOUR", "CHAMPION")
        return ("CHAMPION",)

    async def load_battles(
        self, run_id: UUID, *, battle_number: int | None = None
    ) -> list[tuple[Battle, TrainerTeam, Trainer]]:
        statement = (
            select(Battle, TrainerTeam, Trainer)
            .join(TrainerTeam, TrainerTeam.id == Battle.trainer_team_id)
            .join(Trainer, Trainer.id == TrainerTeam.trainer_id)
            .where(Battle.run_id == run_id)
            .order_by(Battle.battle_number)
        )
        if battle_number is not None:
            statement = statement.where(Battle.battle_number == battle_number)
        result = await self._session.execute(statement)
        return list(result.all())

    async def to_battle_views(
        self, rows: list[tuple[Battle, TrainerTeam, Trainer]]
    ) -> tuple[BattleView, ...]:
        if not rows:
            return ()
        trainer_team_ids = [trainer_team.id for _, trainer_team, _ in rows]
        pokemon_rows = await self._session.execute(
            select(TrainerTeamPokemon, Pokemon)
            .join(Pokemon, Pokemon.id == TrainerTeamPokemon.pokemon_id)
            .where(TrainerTeamPokemon.trainer_team_id.in_(trainer_team_ids))
            .order_by(TrainerTeamPokemon.trainer_team_id, TrainerTeamPokemon.slot_number)
        )
        pokemon_by_team: dict[UUID, list[OpponentPokemonView]] = {}
        for member, pokemon in pokemon_rows.all():
            pokemon_by_team.setdefault(member.trainer_team_id, []).append(
                OpponentPokemonView(
                    slot_number=member.slot_number,
                    pokemon_id=pokemon.id,
                    name=pokemon.name,
                    form_name=pokemon.form_name,
                    primary_type=pokemon.primary_type,
                    secondary_type=pokemon.secondary_type,
                    nature=member.nature,
                    ability=member.ability,
                    held_item=member.held_item,
                    moves=member.moves,
                    evs=member.evs,
                    ivs=member.ivs,
                )
            )
        return tuple(
            BattleView(
                id=battle.id,
                battle_number=battle.battle_number,
                stage=battle.stage,
                status=battle.status,
                trainer_id=trainer.id,
                trainer_name=trainer.name,
                trainer_sprite_url=trainer.sprite_url,
                trainer_team_id=trainer_team.id,
                team_key=trainer_team.team_key,
                team_category=trainer_team.category,
                simulator_result=battle.simulator_result,
                run_result=battle.run_result,
                request_snapshot=battle.request_snapshot,
                opponent_team=tuple(pokemon_by_team.get(trainer_team.id, [])),
            )
            for battle, trainer_team, trainer in rows
        )
