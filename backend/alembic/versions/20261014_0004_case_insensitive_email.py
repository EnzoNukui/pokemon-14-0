"""Enforce case-insensitive uniqueness for account emails.

Revision ID: 20261014_0004
Revises: 20261014_0003
"""

from typing import Sequence, Union

from alembic import op

revision: str = "20261014_0004"
down_revision: Union[str, None] = "20261014_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS uq_users_email_lower ON users (lower(email))"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS uq_users_email_lower")
