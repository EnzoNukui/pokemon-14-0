from decimal import Decimal
import unittest

from app.modules.battles.domain.outcomes import (
    RunBattleResult,
    SimulatorResult,
    resolve_run_battle_result,
)
from app.modules.runs.domain.draft_policy import DraftProbabilityPolicy
from app.modules.runs.domain.rules import (
    TOTAL_BATTLES,
    advance_run,
    stage_for_battle_number,
    stage_for_progress,
)
from app.modules.runs.domain.states import RunStage, RunStatus


class RunRulesTests(unittest.TestCase):
    def test_battle_path_has_the_expected_stage_boundaries(self) -> None:
        self.assertEqual(stage_for_battle_number(1), RunStage.GYM)
        self.assertEqual(stage_for_battle_number(8), RunStage.GYM)
        self.assertEqual(stage_for_battle_number(9), RunStage.ELITE_FOUR)
        self.assertEqual(stage_for_battle_number(12), RunStage.ELITE_FOUR)
        self.assertEqual(stage_for_battle_number(13), RunStage.CHAMPION)
        self.assertEqual(TOTAL_BATTLES, 13)
        self.assertEqual(stage_for_progress(13), RunStage.FINISHED)

    def test_draw_counts_as_a_loss_and_fails_the_run(self) -> None:
        transition = advance_run(0, SimulatorResult.DRAW)

        self.assertEqual(transition.result, RunBattleResult.LOSS)
        self.assertEqual(transition.status, RunStatus.FAILED)
        self.assertEqual(transition.progress_index, 1)

    def test_winning_the_thirteenth_battle_completes_the_run(self) -> None:
        transition = advance_run(12, SimulatorResult.WIN)

        self.assertEqual(transition.status, RunStatus.COMPLETED)
        self.assertEqual(transition.stage, RunStage.FINISHED)
        self.assertEqual(transition.progress_index, 13)

    def test_invalid_battle_numbers_and_progress_are_rejected(self) -> None:
        for number in (0, 14):
            with self.subTest(number=number), self.assertRaises(ValueError):
                stage_for_battle_number(number)
        with self.assertRaises(ValueError):
            advance_run(13, SimulatorResult.WIN)


class DraftPolicyTests(unittest.TestCase):
    def test_approved_tier_weights_total_99_percent(self) -> None:
        policy = DraftProbabilityPolicy(
            tier_weights={
                1: Decimal("0.12"),
                2: Decimal("0.32"),
                3: Decimal("0.40"),
                4: Decimal("0.10"),
                5: Decimal("0.05"),
            }
        )

        self.assertEqual(sum(policy.tier_weights.values()), Decimal("0.99"))

    def test_policy_rejects_weights_that_do_not_total_99_percent(self) -> None:
        with self.assertRaises(ValueError):
            DraftProbabilityPolicy(
                tier_weights={tier: Decimal("0.20") for tier in range(1, 6)}
            )


if __name__ == "__main__":
    unittest.main()
