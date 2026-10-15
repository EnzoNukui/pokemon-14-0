import unittest

from sqlalchemy import UniqueConstraint

from app.db.base import Base
from app.db import models  # noqa: F401 - registers all mapped tables


class DatabaseMetadataTests(unittest.TestCase):
    def test_expected_schema_tables_are_registered(self) -> None:
        self.assertEqual(
            set(Base.metadata.tables),
            {
                "users",
                "pokemon",
                "pokemon_builds",
                "trainers",
                "trainer_teams",
                "trainer_team_pokemon",
                "runs",
                "run_draft_options",
                "teams",
                "team_pokemon",
                "battles",
                "hall_of_fame",
                "champion_history",
                "current_champion",
            },
        )

    def test_battle_schema_does_not_archive_protocol_logs(self) -> None:
        self.assertNotIn("raw_log", Base.metadata.tables["battles"].columns)

    def test_database_enforces_one_active_run_per_user(self) -> None:
        indexes = Base.metadata.tables["runs"].indexes
        active_run_index = next(
            index for index in indexes if index.name == "uq_runs_one_active_per_user"
        )

        self.assertTrue(active_run_index.unique)
        self.assertIn("ACTIVE", str(active_run_index.dialect_options["postgresql"]["where"]))

    def test_trainer_team_allows_duplicate_species_but_unique_slots(self) -> None:
        constraints = Base.metadata.tables["trainer_team_pokemon"].constraints
        unique_columns = {
            tuple(column.name for column in constraint.columns)
            for constraint in constraints
            if isinstance(constraint, UniqueConstraint)
        }

        self.assertIn(("trainer_team_id", "slot_number"), unique_columns)
        self.assertNotIn(("trainer_team_id", "pokemon_id"), unique_columns)

    def test_player_team_prevents_duplicate_species(self) -> None:
        constraints = Base.metadata.tables["team_pokemon"].constraints
        unique_columns = {
            tuple(column.name for column in constraint.columns)
            for constraint in constraints
            if isinstance(constraint, UniqueConstraint)
        }

        self.assertIn(("team_id", "pokemon_id"), unique_columns)


if __name__ == "__main__":
    unittest.main()
