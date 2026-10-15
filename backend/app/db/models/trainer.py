from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Trainer(TimestampMixin, Base):
    __tablename__ = "trainers"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    region: Mapped[str | None] = mapped_column(String(80))
    sprite_url: Mapped[str | None] = mapped_column(String(500))
    sprite_source: Mapped[str | None] = mapped_column(String(160))
    sprite_credit: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)


class TrainerTeam(TimestampMixin, Base):
    __tablename__ = "trainer_teams"
    __table_args__ = (
        UniqueConstraint("trainer_id", "team_key", name="uq_trainer_teams_trainer_team_key"),
        CheckConstraint(
            "category IN ('GYM_LEADER', 'ELITE_FOUR', 'CHAMPION', 'OTHER')",
            name="category_values",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    trainer_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("trainers.id", ondelete="RESTRICT"), nullable=False
    )
    team_key: Mapped[str] = mapped_column(String(80), nullable=False)
    category: Mapped[str] = mapped_column(String(24), nullable=False)
    difficulty_tier: Mapped[str | None] = mapped_column(String(24))
    anime_period: Mapped[str] = mapped_column(String(160), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(1000))
    source_notes: Mapped[str | None] = mapped_column(Text)
    ai_profile: Mapped[dict[str, object]] = mapped_column(
        JSONB, nullable=False, default=dict, server_default=text("'{}'::jsonb")
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )


class TrainerTeamPokemon(Base):
    __tablename__ = "trainer_team_pokemon"
    __table_args__ = (
        UniqueConstraint("trainer_team_id", "slot_number", name="uq_trainer_team_pokemon_slot"),
        CheckConstraint("slot_number BETWEEN 1 AND 6", name="slot_number_range"),
        CheckConstraint(
            "jsonb_typeof(moves) = 'array' AND jsonb_array_length(moves) BETWEEN 1 AND 4",
            name="one_to_four_moves",
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    trainer_team_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("trainer_teams.id", ondelete="CASCADE"),
        nullable=False,
    )
    pokemon_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pokemon.id", ondelete="RESTRICT"), nullable=False
    )
    slot_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    nature: Mapped[str] = mapped_column(String(40), nullable=False)
    ability: Mapped[str] = mapped_column(String(80), nullable=False)
    held_item: Mapped[str | None] = mapped_column(String(80))
    moves: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    evs: Mapped[dict[str, int]] = mapped_column(JSONB, nullable=False)
    ivs: Mapped[dict[str, int]] = mapped_column(JSONB, nullable=False)
