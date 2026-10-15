from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    SmallInteger,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Team(TimestampMixin, Base):
    __tablename__ = "teams"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    run_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("runs.id", ondelete="RESTRICT"), nullable=False, unique=True
    )


class TeamPokemon(Base):
    __tablename__ = "team_pokemon"
    __table_args__ = (
        UniqueConstraint("team_id", "slot_number", name="uq_team_pokemon_slot"),
        UniqueConstraint("team_id", "pokemon_id", name="uq_team_pokemon_species"),
        CheckConstraint("slot_number BETWEEN 1 AND 6", name="slot_number_range"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    team_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    pokemon_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pokemon.id", ondelete="RESTRICT"), nullable=False
    )
    pokemon_build_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pokemon_builds.id", ondelete="RESTRICT"), nullable=False
    )
    slot_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    build_snapshot: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)
