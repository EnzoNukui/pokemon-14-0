"""Allow official trainer teams to contain the same species in multiple slots.

Revision ID: 20261014_0005
Revises: 20261014_0004
"""

from typing import Sequence, Union

from alembic import op

revision: str = "20261014_0005"
down_revision: Union[str, None] = "20261014_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # The bootstrap revision builds from current ORM metadata. On a fresh
    # database that metadata may already omit this constraint, so make this
    # historical cleanup safe in both the old and current schema states.
    op.execute(
        "ALTER TABLE trainer_team_pokemon "
        "DROP CONSTRAINT IF EXISTS uq_trainer_team_pokemon_species"
    )


def downgrade() -> None:
    op.create_unique_constraint(
        "uq_trainer_team_pokemon_species",
        "trainer_team_pokemon",
        ["trainer_team_id", "pokemon_id"],
    )
