from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class WorkoutSessionItem(Base):
    __tablename__ = "workout_session_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("workout_sessions.id", ondelete="CASCADE"), nullable=False)
    activity_type_id: Mapped[int] = mapped_column(ForeignKey("activity_types.id"), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)

    session = relationship("WorkoutSession", back_populates="items")
    activity_type = relationship("ActivityType")
    measurements = relationship("WorkoutSessionMeasurement", back_populates="session_item", cascade="all, delete-orphan")
