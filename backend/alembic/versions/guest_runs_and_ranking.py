"""Allow guest-owned runs and claim only completed runs for ranking.

Revision ID: guest_runs_and_ranking
Revises: 20261015_0009
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "guest_runs_and_ranking"
down_revision: Union[str, None] = "20261015_0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "guest_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column(
            "expires_at", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_guest_sessions")),
        sa.UniqueConstraint("token_hash", name=op.f("uq_guest_sessions_token_hash")),
    )
    op.create_index(
        op.f("ix_guest_sessions_expires_at"), "guest_sessions", ["expires_at"], unique=False
    )

    op.alter_column(
        "runs", "user_id", existing_type=sa.Uuid(), existing_nullable=False, nullable=True
    )
    op.add_column("runs", sa.Column("guest_session_id", sa.Uuid(), nullable=True))
    op.create_foreign_key(
        op.f("fk_runs_guest_session_id_guest_sessions"),
        "runs",
        "guest_sessions",
        ["guest_session_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_check_constraint(
        "exactly_one_owner",
        "runs",
        "(user_id IS NOT NULL AND guest_session_id IS NULL) OR "
        "(user_id IS NULL AND guest_session_id IS NOT NULL)",
    )
    op.drop_index("uq_runs_one_active_per_user", table_name="runs")
    op.create_index(
        "uq_runs_one_active_per_user",
        "runs",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("status = 'ACTIVE' AND user_id IS NOT NULL"),
    )
    op.create_index(
        "uq_runs_one_active_per_guest_session",
        "runs",
        ["guest_session_id"],
        unique=True,
        postgresql_where=sa.text("status = 'ACTIVE' AND guest_session_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("uq_runs_one_active_per_guest_session", table_name="runs")
    op.drop_index("uq_runs_one_active_per_user", table_name="runs")
    op.create_index(
        "uq_runs_one_active_per_user",
        "runs",
        ["user_id"],
        unique=True,
        postgresql_where=sa.text("status = 'ACTIVE'"),
    )
    op.drop_constraint(op.f("ck_runs_exactly_one_owner"), "runs", type_="check")
    op.drop_constraint(op.f("fk_runs_guest_session_id_guest_sessions"), "runs", type_="foreignkey")
    op.drop_column("runs", "guest_session_id")
    op.alter_column(
        "runs", "user_id", existing_type=sa.Uuid(), existing_nullable=True, nullable=False
    )
    op.drop_index(op.f("ix_guest_sessions_expires_at"), table_name="guest_sessions")
    op.drop_table("guest_sessions")
