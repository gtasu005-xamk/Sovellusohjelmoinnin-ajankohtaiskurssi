from datetime import datetime, timezone
from sqlalchemy import Boolean, CheckConstraint, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Goal(Base):
    __tablename__ = "goals"
    __table_args__ = (
        CheckConstraint("period IN ('week', 'month')", name="ck_goal_period"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    unit_type_id: Mapped[int] = mapped_column(ForeignKey("unit_types.id"), nullable=False)
    activity_type_id: Mapped[int | None] = mapped_column(ForeignKey("activity_types.id"), nullable=True)
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    period: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    unit_type = relationship("UnitType")
    activity_type = relationship("ActivityType")