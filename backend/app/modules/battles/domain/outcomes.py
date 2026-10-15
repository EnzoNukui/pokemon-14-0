from enum import Enum


class SimulatorResult(str, Enum):
    """Raw result returned by the battle simulator."""

    WIN = "WIN"
    LOSS = "LOSS"
    DRAW = "DRAW"


class RunBattleResult(str, Enum):
    """Result that the game applies to the player's run."""

    WIN = "WIN"
    LOSS = "LOSS"


def resolve_run_battle_result(result: SimulatorResult) -> RunBattleResult:
    """Convert the simulator result into the agreed run result; a draw is a loss."""
    if result is SimulatorResult.WIN:
        return RunBattleResult.WIN
    return RunBattleResult.LOSS
