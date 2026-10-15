from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    SmallInteger,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Battle(TimestampMixin, Base):
    __tablename__ = "battles"
    __table_args__ = (
        UniqueConstraint("run_id", "battle_number", name="uq_battles_run_number"),
        CheckConstraint("battle_number BETWEEN 1 AND 13", name="battle_number_range"),
        CheckConstraint(
            "stage IN ('GYM', 'ELITE_FOUR', 'CHAMPION')", name="stage_values"
        ),
        CheckConstraint(
            "status IN ('PENDING', 'RUNNING', 'COMPLETED', 'ENGINE_ERROR', 'ABANDONED')",
            name="status_values",
        ),
        CheckConstraint(
            "simulator_result IS NULL OR simulator_result IN ('WIN', 'LOSS', 'DRAW')",
            name="simulator_result_values",
        ),
        CheckConstraint(
            "run_result IS NULL OR run_result IN ('WIN', 'LOSS')", name="run_result_values"
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    run_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("runs.id", ondelete="RESTRICT"), nullable=False
    )
    trainer_team_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("trainer_teams.id", ondelete="RESTRICT"),
        nullable=False,
    )
    battle_number: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    stage: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), nullable=False, default="PENDING", server_default=text("'PENDING'")
    )
    simulator_result: Mapped[str | None] = mapped_column(String(8))
    run_result: Mapped[str | None] = mapped_column(String(4))
    battle_format: Mapped[str | None] = mapped_column(String(100))
    engine_version: Mapped[str | None] = mapped_column(String(40))
    request_snapshot: Mapped[dict[str, object] | None] = mapped_column(JSONB)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
