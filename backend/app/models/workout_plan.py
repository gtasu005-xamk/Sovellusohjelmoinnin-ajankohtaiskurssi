from datetime import date, datetime, timezone
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

# Ohjelma, johon sessiot kuuluvat workout_sessions.plan_id:n kautta (ei liitostaulua).
# start_date ja length_weeks ovat pelkkää metatietoa, ei toistoja.
class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    length_weeks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                 default=lambda: datetime.now(timezone.utc),
                 onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    sessions = relationship("WorkoutSession", back_populates="plan",
                            order_by="WorkoutSession.session_at.asc().nulls_last()")

    def __str__(self):
        return self.name
