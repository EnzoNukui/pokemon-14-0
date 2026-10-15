"""Create the initial Pokémon 13-0 database schema.

Revision ID: 20261014_0001
Revises:
Create Date: 2026-10-14

This is the bootstrap revision, so it creates the complete metadata registered by
the ORM models. Future revisions should contain explicit Alembic operations and
must not edit this revision after it has been applied to a shared database.
"""

from typing import Sequence, Union

from alembic import op

from app.db.base import Base
import app.db.models  # noqa: F401 - register every table before create_all/drop_all

revision: str = "20261014_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all initial tables, constraints, and indexes."""
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    """Drop all tables created by the bootstrap revision."""
    Base.metadata.drop_all(bind=op.get_bind())
