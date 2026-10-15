from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Pokemon(TimestampMixin, Base):
    __tablename__ = "pokemon"
    __table_args__ = (
        CheckConstraint("generation BETWEEN 1 AND 99", name="generation_range"),
        CheckConstraint(
            "draft_tier IS NULL OR draft_tier BETWEEN 1 AND 5", name="draft_tier_range"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    external_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    form_name: Mapped[str | None] = mapped_column(String(100))
    national_dex_number: Mapped[int | None] = mapped_column(Integer)
    generation: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    primary_type: Mapped[str] = mapped_column(String(20), nullable=False)
    secondary_type: Mapped[str | None] = mapped_column(String(20))
    base_stats: Mapped[dict[str, int]] = mapped_column(JSONB, nullable=False)
    is_legendary: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    is_mythical: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    is_pseudo_legendary: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    is_draft_eligible: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
    draft_tier: Mapped[int | None] = mapped_column(SmallInteger)
    competitive_tier: Mapped[str | None] = mapped_column(String(20))
    front_sprite_url: Mapped[str | None] = mapped_column(String(500))
    back_sprite_url: Mapped[str | None] = mapped_column(String(500))
    cry_url: Mapped[str | None] = mapped_column(String(500))
    data_source: Mapped[str | None] = mapped_column(String(100))


class PokemonBuild(TimestampMixin, Base):
    __tablename__ = "pokemon_builds"
    __table_args__ = (
        UniqueConstraint("pokemon_id", "build_key", name="uq_pokemon_builds_pokemon_build_key"),
        CheckConstraint(
            "jsonb_typeof(moves) = 'array' AND jsonb_array_length(moves) BETWEEN 1 AND 4",
            name="one_to_four_moves",
        ),
        CheckConstraint(
            "validation_status IN ('PENDING', 'VALID', 'INVALID')",
            name="validation_status_values",
        ),
        CheckConstraint(
            "NOT is_default OR (validation_status = 'VALID' AND validated_format IS NOT NULL AND validated_at IS NOT NULL)",
            name="default_requires_showdown_validation",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    pokemon_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pokemon.id", ondelete="RESTRICT"), nullable=False
    )
    build_key: Mapped[str] = mapped_column(String(80), nullable=False)
    nature: Mapped[str] = mapped_column(String(40), nullable=False)
    ability: Mapped[str] = mapped_column(String(80), nullable=False)
    held_item: Mapped[str | None] = mapped_column(String(80))
    moves: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    evs: Mapped[dict[str, int]] = mapped_column(JSONB, nullable=False)
    ivs: Mapped[dict[str, int]] = mapped_column(JSONB, nullable=False)
    validation_status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="PENDING", server_default=text("'PENDING'")
    )
    validated_format: Mapped[str | None] = mapped_column(String(60))
    validation_errors: Mapped[list[str]] = mapped_column(
        JSONB, nullable=False, default=list, server_default=text("'[]'::jsonb")
    )
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_default: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
