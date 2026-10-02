from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class WorkoutSession(Base):
    __tablename__ = "workout_sessions"
    __table_args__ = (
        CheckConstraint("status IN ('planned', 'in_progress', 'completed')", name="ck_workout_session_status"),
        CheckConstraint("intensity BETWEEN 1 AND 10", name="ck_workout_session_intensity"),
        Index("ix_workout_sessions_user_id_session_at", "user_id", "session_at"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    session_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String, default="planned", nullable=False)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    intensity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_session_id: Mapped[int | None] = mapped_column(
        ForeignKey("workout_sessions.id", ondelete="SET NULL"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 default=lambda: datetime.now(timezone.utc),
                                                 onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    items = relationship("WorkoutSessionItem", back_populates="session",cascade="all, delete-orphan", order_by="WorkoutSessionItem.sort_order")

    def __str__(self):
        return self.name
