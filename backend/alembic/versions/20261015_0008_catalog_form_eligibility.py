"""Track base Pokémon versus trainer-only alternate forms.

Revision ID: 20261015_0008
Revises: 20261015_0007
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261015_0008"
down_revision: Union[str, None] = "20261015_0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # The bootstrap migration builds from current ORM metadata, so fresh
    # databases may already include columns introduced by later revisions.
    op.execute(
        "ALTER TABLE pokemon ADD COLUMN IF NOT EXISTS "
        "is_draft_eligible BOOLEAN NOT NULL DEFAULT true"
    )


def downgrade() -> None:
    op.execute("ALTER TABLE pokemon DROP COLUMN IF EXISTS is_draft_eligible")
