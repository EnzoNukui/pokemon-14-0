from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class HallOfFame(Base):
    __tablename__ = "hall_of_fame"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    run_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("runs.id", ondelete="RESTRICT"), nullable=False, unique=True
    )
    user_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    team_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("teams.id", ondelete="RESTRICT"), nullable=False
    )
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    performance_snapshot: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)


class ChampionHistory(Base):
    __tablename__ = "champion_history"
    __table_args__ = (
        CheckConstraint(
            "(team_id IS NOT NULL AND trainer_team_id IS NULL) OR "
            "(team_id IS NULL AND trainer_team_id IS NOT NULL)",
            name="exactly_one_team_source",
        ),
        UniqueConstraint("run_id", name="uq_champion_history_run"),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT")
    )
    team_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("teams.id", ondelete="RESTRICT")
    )
    trainer_team_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("trainer_teams.id", ondelete="RESTRICT")
    )
    run_id: Mapped[UUID | None] = mapped_column(
        Uuid(as_uuid=True), ForeignKey("runs.id", ondelete="RESTRICT")
    )
    became_champion_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    lost_championship_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class CurrentChampion(Base):
    __tablename__ = "current_champion"
    __table_args__ = (
        CheckConstraint("singleton_id = 1", name="one_current_champion_row"),
    )

    singleton_id: Mapped[int] = mapped_column(
        SmallInteger, primary_key=True, default=1, server_default=text("1")
    )
    champion_history_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("champion_history.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
