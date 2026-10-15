"""Track Showdown validation for generated Pokémon builds.

Revision ID: 20261014_0002
Revises: 20261014_0001
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261014_0002"
down_revision: Union[str, None] = "20261014_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TABLE pokemon_builds ADD COLUMN IF NOT EXISTS "
        "validation_status VARCHAR(16) NOT NULL DEFAULT 'PENDING'"
    )
    op.execute(
        "ALTER TABLE pokemon_builds ADD COLUMN IF NOT EXISTS validated_format VARCHAR(60)"
    )
    op.execute(
        "ALTER TABLE pokemon_builds ADD COLUMN IF NOT EXISTS "
        "validation_errors JSONB NOT NULL DEFAULT '[]'::jsonb"
    )
    op.execute(
        "ALTER TABLE pokemon_builds ADD COLUMN IF NOT EXISTS validated_at TIMESTAMPTZ"
    )
    op.execute(
        """DO $$ BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'validation_status_values') THEN
            ALTER TABLE pokemon_builds ADD CONSTRAINT validation_status_values
            CHECK (validation_status IN ('PENDING', 'VALID', 'INVALID'));
        END IF;
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'default_requires_showdown_validation') THEN
            ALTER TABLE pokemon_builds ADD CONSTRAINT default_requires_showdown_validation
            CHECK (NOT is_default OR (validation_status = 'VALID' AND validated_format IS NOT NULL AND validated_at IS NOT NULL));
        END IF;
        END $$"""
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE pokemon_builds DROP CONSTRAINT IF EXISTS "
        "default_requires_showdown_validation"
    )
    op.execute(
        "ALTER TABLE pokemon_builds DROP CONSTRAINT IF EXISTS validation_status_values"
    )
    op.execute("ALTER TABLE pokemon_builds DROP COLUMN IF EXISTS validated_at")
    op.execute("ALTER TABLE pokemon_builds DROP COLUMN IF EXISTS validation_errors")
    op.execute("ALTER TABLE pokemon_builds DROP COLUMN IF EXISTS validated_format")
    op.execute("ALTER TABLE pokemon_builds DROP COLUMN IF EXISTS validation_status")
