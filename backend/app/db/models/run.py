from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Run(TimestampMixin, Base):
    __tablename__ = "runs"
    __table_args__ = (
        CheckConstraint(
            "status IN ('ACTIVE', 'FAILED', 'COMPLETED', 'ABANDONED')", name="status_values"
        ),
        CheckConstraint(
            "stage IN ('DRAFT', 'GYM', 'ELITE_FOUR', 'CHAMPION', 'FINISHED')",
            name="stage_values",
        ),
        CheckConstraint("progress_index BETWEEN 0 AND 13", name="progress_index_range"),
        Index(
            "uq_runs_one_active_per_user",
            "user_id",
            unique=True,
            postgresql_where=text("status = 'ACTIVE'"),
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="ACTIVE", server_default=text("'ACTIVE'")
    )
    stage: Mapped[str] = mapped_column(
        String(16), nullable=False, default="DRAFT", server_default=text("'DRAFT'")
    )
    progress_index: Mapped[int] = mapped_column(
        SmallInteger, nullable=False, default=0, server_default=text("0")
    )
    reroll_used: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    legendary_selected: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    random_seed: Mapped[int | None] = mapped_column(BigInteger)
    version: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1, server_default=text("1")
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class RunDraftOption(Base):
    __tablename__ = "run_draft_options"
    __table_args__ = (
        UniqueConstraint(
            "run_id", "round_number", "display_set", "option_number",
            name="uq_draft_options_round_set_slot",
        ),
        UniqueConstraint("run_id", "pokemon_id", name="uq_draft_options_pokemon_per_run"),
        CheckConstraint("round_number BETWEEN 1 AND 6", name="round_number_range"),
        CheckConstraint("display_set IN (0, 1)", name="display_set_values"),
        CheckConstraint("option_number BETWEEN 1 AND 6", name="option_number_range"),
        CheckConstraint(
            "resolution IN ('PENDING', 'SELECTED', 'REJECTED', 'REROLLED')",
            name="resolution_values",
        ),
        Index(
            "uq_draft_options_one_selection_per_round",
            "run_id",
            "round_number",
            unique=True,
            postgresql_where=text("resolution = 'SELECTED'"),
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    run_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("runs.id", ondelete="CASCADE"), nullable=False
    )
    pokemon_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("pokemon.id", ondelete="RESTRICT"), nullable=False
    )
    round_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    display_set: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    option_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    resolution: Mapped[str] = mapped_column(
        String(12), nullable=False, default="PENDING", server_default=text("'PENDING'")
    )
