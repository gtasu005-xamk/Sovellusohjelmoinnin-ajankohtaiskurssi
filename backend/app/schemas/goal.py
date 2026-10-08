from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

GoalPeriod = Literal["week", "month"]


class GoalCreate(BaseModel):
    unit_type_id: int
    activity_type_id: int | None = None
    target_value: float = Field(gt=0)
    period: GoalPeriod
    active: bool = True


class GoalUpdate(BaseModel):
    unit_type_id: int = None
    activity_type_id: int | None = None
    target_value: float = Field(default=None, gt=0)
    period: GoalPeriod = None
    active: bool = None


class GoalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    unit_type_id: int
    activity_type_id: int | None
    target_value: float
    period: str
    active: bool
    created_at: datetime
