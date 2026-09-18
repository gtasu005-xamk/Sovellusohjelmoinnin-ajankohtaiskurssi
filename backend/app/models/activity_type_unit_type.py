from sqlalchemy import Boolean, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class ActivityTypeUnitType(Base):
    __tablename__ = "activity_type_unit_types"
    __table_args__ = (UniqueConstraint("activity_type_id", "unit_type_id", name="uq_activity_type_unit_type"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    activity_type_id: Mapped[int] = mapped_column(ForeignKey("activity_types.id"), nullable=False)
    unit_type_id: Mapped[int] = mapped_column(ForeignKey("unit_types.id"),nullable=False,)

    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    per_set: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    activity_type = relationship("ActivityType",back_populates="unit_links", )

    unit_type = relationship( "UnitType", back_populates="activity_links",)