from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class WorkoutSessionMeasurement(Base):
    __tablename__ = "workout_session_measurements"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_item_id: Mapped[int] = mapped_column(
        ForeignKey("workout_session_items.id", ondelete="CASCADE"), nullable=False)
    unit_type_id: Mapped[int] = mapped_column(ForeignKey("unit_types.id"), nullable=False)
    planned_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    actual_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    set_index: Mapped[int | None] = mapped_column(Integer, nullable=True)
    session_item = relationship("WorkoutSessionItem", back_populates="measurements")
    unit_type = relationship("UnitType")
