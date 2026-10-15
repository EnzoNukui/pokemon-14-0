"""Allow a running battle to close when its run is abandoned.

Revision ID: 20261015_0006
Revises: 20261014_0005
"""

from typing import Sequence, Union

from alembic import op

revision: str = "20261015_0006"
down_revision: Union[str, None] = "20261014_0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Mark this as an already-rendered name so the metadata convention does not
    # prepend ``ck_battles_`` a second time.
    op.drop_constraint(op.f("ck_battles_status_values"), "battles", type_="check")
    op.create_check_constraint(
        "status_values",
        "battles",
        "status IN ('PENDING', 'RUNNING', 'COMPLETED', 'ENGINE_ERROR', 'ABANDONED')",
    )


def downgrade() -> None:
    op.execute("UPDATE battles SET status = 'ENGINE_ERROR' WHERE status = 'ABANDONED'")
    op.drop_constraint(op.f("ck_battles_status_values"), "battles", type_="check")
    op.create_check_constraint(
        "status_values",
        "battles",
        "status IN ('PENDING', 'RUNNING', 'COMPLETED', 'ENGINE_ERROR')",
    )
