"""Store a trainer name on each account.

Revision ID: 20261015_0010
Revises: 20261015_0009
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261015_0010"
down_revision: Union[str, None] = "20261015_0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("trainer_name", sa.String(length=24), nullable=True))
    op.execute("UPDATE users SET trainer_name = left(split_part(email, '@', 1), 24)")
    op.alter_column("users", "trainer_name", nullable=False)


def downgrade() -> None:
    op.drop_column("users", "trainer_name")
