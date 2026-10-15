"""Allow storing selected rivals and other notable trainers.

Revision ID: 20261015_0009
Revises: 20261015_0008
"""

from typing import Sequence, Union

from alembic import op

revision: str = "20261015_0009"
down_revision: Union[str, None] = "20261015_0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f("ck_trainer_teams_category_values"), "trainer_teams", type_="check")
    op.create_check_constraint(
        "category_values",
        "trainer_teams",
        "category IN ('GYM_LEADER', 'ELITE_FOUR', 'CHAMPION', 'OTHER')",
    )


def downgrade() -> None:
    op.drop_constraint(op.f("ck_trainer_teams_category_values"), "trainer_teams", type_="check")
    op.create_check_constraint(
        "category_values",
        "trainer_teams",
        "category IN ('GYM_LEADER', 'ELITE_FOUR', 'CHAMPION')",
    )
