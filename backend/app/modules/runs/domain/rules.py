from dataclasses import dataclass
from decimal import Decimal

from app.modules.battles.domain.outcomes import (
    RunBattleResult,
    SimulatorResult,
    resolve_run_battle_result,
)
from app.modules.runs.domain.states import RunStage, RunStatus

DRAFT_ROUNDS = 6
DRAFT_OPTIONS_PER_ROUND = 6
REROLLS_PER_RUN = 1
MAX_LEGENDARY_OR_MYTHICAL_PER_TEAM = 1
LEGENDARY_OFFER_PROBABILITY = Decimal("0.01")

GYM_BATTLES = 8
ELITE_FOUR_BATTLES = 4
CHAMPION_BATTLES = 1
TOTAL_BATTLES = GYM_BATTLES + ELITE_FOUR_BATTLES + CHAMPION_BATTLES


@dataclass(frozen=True, slots=True)
class RunTransition:
    status: RunStatus
    stage: RunStage
    progress_index: int
    result: RunBattleResult


def stage_for_progress(progress_index: int) -> RunStage:
    """Return the next/just-played stage for a run's completed battle count."""
    if not 0 <= progress_index <= TOTAL_BATTLES:
        raise ValueError(f"progress_index must be between 0 and {TOTAL_BATTLES}")
    if progress_index == TOTAL_BATTLES:
        return RunStage.FINISHED
    if progress_index < GYM_BATTLES:
        return RunStage.GYM
    if progress_index < GYM_BATTLES + ELITE_FOUR_BATTLES:
        return RunStage.ELITE_FOUR
    return RunStage.CHAMPION


def stage_for_battle_number(battle_number: int) -> RunStage:
    """Return the stage for a one-based opponent position in the 13-battle path."""
    if not 1 <= battle_number <= TOTAL_BATTLES:
        raise ValueError(f"battle_number must be between 1 and {TOTAL_BATTLES}")
    return stage_for_progress(battle_number - 1)


def advance_run(progress_index: int, simulator_result: SimulatorResult) -> RunTransition:
    """Apply one simulator result to the run's progress and terminal state."""
    if not 0 <= progress_index < TOTAL_BATTLES:
        raise ValueError(f"progress_index must be between 0 and {TOTAL_BATTLES - 1}")

    run_result = resolve_run_battle_result(simulator_result)
    next_progress = progress_index + 1
    if run_result is RunBattleResult.LOSS:
        status = RunStatus.FAILED
    elif next_progress == TOTAL_BATTLES:
        status = RunStatus.COMPLETED
    else:
        status = RunStatus.ACTIVE

    return RunTransition(
        status=status,
        stage=stage_for_progress(next_progress),
        progress_index=next_progress,
        result=run_result,
    )
