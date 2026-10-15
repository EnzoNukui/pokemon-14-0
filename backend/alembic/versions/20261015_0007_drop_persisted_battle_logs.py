"""Keep Showdown protocol events transient instead of archiving full logs.

Revision ID: 20261015_0007
Revises: 20261015_0006
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261015_0007"
down_revision: Union[str, None] = "20261015_0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Protocol events are returned to the client during a battle. Run and battle
    # outcomes remain in their existing tables, so archived event rows/logs are
    # redundant and grow with every turn.
    op.execute("DROP TABLE IF EXISTS battle_events")
    op.execute("ALTER TABLE battles DROP COLUMN IF EXISTS raw_log")


def downgrade() -> None:
    # This recreates the old schema only; discarded protocol history cannot be
    # restored by a downgrade.
    op.add_column("battles", sa.Column("raw_log", sa.Text(), nullable=True))
    op.create_table(
        "battle_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("battle_id", sa.Uuid(), nullable=False),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint("sequence_number >= 1", name="ck_battle_events_sequence_number_positive"),
        sa.ForeignKeyConstraint(["battle_id"], ["battles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "battle_id", "sequence_number", name="uq_battle_events_sequence"
        ),
    )
