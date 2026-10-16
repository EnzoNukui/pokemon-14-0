"""Coordinate one battle result with the owning run's progression."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.battle import Battle
from app.db.models.run import Run
from app.modules.battles.application.battle_service import BattleService
from app.modules.battles.application.errors import (
    BattleEngineResponseError,
    BattleEngineUnavailable,
)
from app.modules.battles.infrastructure.showdown_client import ShowdownClient
from app.modules.championship.application.championship_service import (
    ChampionshipConfigurationError,
    record_run_completion,
)
from app.modules.runs.application.battle_errors import (
    BattleOrderConflict,
    BattlePathConfigurationError,
    BattleProgressionError,
    BattleProgressionUnavailable,
    BattleRunNotFound,
)
from app.modules.runs.application.battle_path_service import BattlePathService
from app.modules.runs.application.battle_views import (
    BattlePathView,
    BattleTurnView,
    BattleView,
)
from app.modules.runs.domain.rules import TOTAL_BATTLES, advance_run
from app.modules.runs.domain.states import RunStatus
from app.modules.battles.domain.outcomes import SimulatorResult
from app.modules.runs.domain.ownership import RunOwner


class BattleProgressionService:
    """Enforce run ownership/order and apply the simulator's battle result."""

    def __init__(
        self, session: AsyncSession, showdown: ShowdownClient | None = None
    ) -> None:
        self._session = session
        self._path = BattlePathService(session)
        self._battles = BattleService(session, showdown)

    async def start_current_battle(
        self, *, owner: RunOwner, run_id: UUID
    ) -> BattleTurnView:
        async with self._session.begin():
            run = await self._path.get_owned_run(
                owner=owner, run_id=run_id, lock=True
            )
            self._path.require_active_battle_run(run)
            await self._path.ensure_path(run)
            battle_number = run.progress_index + 1
            battle = await self._get_locked_battle(
                run_id=run.id, battle_number=battle_number
            )

            if battle.status == "RUNNING":
                try:
                    engine_result, events = await self._battles.resume(battle)
                except BattleEngineResponseError as exc:
                    raise BattlePathConfigurationError(str(exc)) from exc
                if self._engine_result_is_complete(engine_result):
                    await self._apply_engine_result(run, battle, engine_result)
                await self._session.flush()
                return self._turn_view(run, battle, engine_result, events)
            if battle.status != "PENDING":
                raise BattleOrderConflict(
                    "This battle cannot be started in its current state."
                )

            try:
                engine_result, events = await self._battles.start(
                    battle=battle,
                    run_id=run.id,
                    trainer_team_id=battle.trainer_team_id,
                )
            except BattleEngineResponseError as exc:
                raise BattlePathConfigurationError(str(exc)) from exc
            if self._engine_result_is_complete(engine_result):
                await self._apply_engine_result(run, battle, engine_result)
            await self._session.flush()
            return self._turn_view(run, battle, engine_result, events)

    async def submit_battle_choice(
        self,
        *,
        owner: RunOwner,
        run_id: UUID,
        battle_number: int,
        choice: str,
    ) -> BattleTurnView:
        if not 1 <= battle_number <= TOTAL_BATTLES:
            raise BattleOrderConflict("Battle number must be between 1 and 13.")
        async with self._session.begin():
            run = await self._path.get_owned_run(
                owner=owner, run_id=run_id, lock=True
            )
            self._path.require_active_battle_run(run)
            expected_number = run.progress_index + 1
            if battle_number != expected_number:
                raise BattleOrderConflict(
                    f"Battle {expected_number} is next; battle {battle_number} cannot receive a choice."
                )
            battle = await self._get_locked_battle(
                run_id=run.id, battle_number=battle_number
            )
            if battle.status != "RUNNING":
                raise BattleOrderConflict(
                    "Start this battle before submitting a choice."
                )

            try:
                engine_result, events = await self._battles.submit_choice(
                    battle=battle, choice=choice
                )
            except BattleEngineResponseError as exc:
                raise BattlePathConfigurationError(str(exc)) from exc
            if self._engine_result_is_complete(engine_result):
                await self._apply_engine_result(run, battle, engine_result)
            await self._session.flush()
            return self._turn_view(run, battle, engine_result, events)

    async def get_path(self, *, owner: RunOwner, run_id: UUID) -> BattlePathView:
        return await self._path.get_path(owner=owner, run_id=run_id)

    async def get_current_battle(
        self, *, owner: RunOwner, run_id: UUID
    ) -> BattleView:
        return await self._path.get_current_battle(owner=owner, run_id=run_id)

    @staticmethod
    def _engine_result_is_complete(engine_result: dict[str, object]) -> bool:
        # Some running engine instances report the winner before updating status.
        # A simulator result is only present after Showdown has emitted |win| or |tie|.
        return (
            engine_result.get("status") == "COMPLETED"
            or engine_result.get("simulator_result") is not None
            or BattleProgressionService._has_tie_event(engine_result)
        )

    @staticmethod
    def _has_tie_event(engine_result: dict[str, object]) -> bool:
        events = engine_result.get("events")
        return isinstance(events, list) and any(
            isinstance(event, dict) and event.get("event_type") == "tie"
            for event in events
        )

    async def _get_locked_battle(self, *, run_id: UUID, battle_number: int) -> Battle:
        battle = await self._session.scalar(
            select(Battle)
            .where(Battle.run_id == run_id, Battle.battle_number == battle_number)
            .with_for_update()
        )
        if battle is None:
            raise BattlePathConfigurationError(
                "The next battle is missing from the run path."
            )
        return battle

    async def _apply_engine_result(
        self, run: Run, battle: Battle, engine_result: dict[str, object]
    ) -> None:
        try:
            # The protocol's tie event is authoritative if the engine's summary
            # accidentally reports a winner for the same completed battle.
            raw_result = (
                "DRAW"
                if self._has_tie_event(engine_result)
                else engine_result.get("simulator_result")
            )
            simulator_result = SimulatorResult(raw_result)
        except (TypeError, ValueError) as exc:
            raise BattlePathConfigurationError(
                "Showdown completed the battle without a recognized result."
            ) from exc

        now = datetime.now(timezone.utc)
        transition = advance_run(run.progress_index, simulator_result)
        battle.status = "COMPLETED"
        battle.simulator_result = simulator_result.value
        battle.run_result = transition.result.value
        battle.finished_at = now
        run.progress_index = transition.progress_index
        run.status = transition.status.value
        run.stage = transition.stage.value
        run.version += 1
        if transition.status is not RunStatus.ACTIVE:
            run.ended_at = now
        if transition.status is RunStatus.COMPLETED:
            if run.user_id is not None:
                try:
                    await record_run_completion(
                        self._session, run=run, completed_at=now
                    )
                except ChampionshipConfigurationError as exc:
                    raise BattlePathConfigurationError(str(exc)) from exc

    @staticmethod
    def _turn_view(
        run: Run,
        battle: Battle,
        engine_result: dict[str, object],
        events: tuple[BattleEventView, ...],
    ) -> BattleTurnView:
        result = engine_result.get("simulator_result")
        return BattleTurnView(
            battle_id=battle.id,
            battle_number=battle.battle_number,
            status=battle.status,
            request=engine_result.get("request")
            if isinstance(engine_result.get("request"), dict)
            else None,
            choice_error=engine_result.get("choice_error")
            if isinstance(engine_result.get("choice_error"), str)
            else None,
            events=events,
            simulator_result=result if isinstance(result, str) else None,
            run_result=battle.run_result,
            run_status=run.status,
            run_stage=run.stage,
            progress_index=run.progress_index,
            next_battle_number=(
                run.progress_index + 1
                if run.status == RunStatus.ACTIVE.value
                else None
            ),
        )
