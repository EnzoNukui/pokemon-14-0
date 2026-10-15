"""Keep the upstream Gen VII competitive tier used for draft classification.

Revision ID: 20261014_0003
Revises: 20261014_0002
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261014_0003"
down_revision: Union[str, None] = "20261014_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE pokemon ADD COLUMN IF NOT EXISTS competitive_tier VARCHAR(20)"
    )


def downgrade() -> None:
    op.execute("ALTER TABLE pokemon DROP COLUMN IF EXISTS competitive_tier")
