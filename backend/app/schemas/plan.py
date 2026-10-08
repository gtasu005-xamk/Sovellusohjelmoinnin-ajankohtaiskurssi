from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.session import SessionOut


class PlanCreate(BaseModel):
    name: str = Field(min_length=1)
    notes: str | None = None
    start_date: date | None = None
    length_weeks: int | None = Field(default=None, ge=1)


class PlanUpdate(BaseModel):
    name: str = Field(default=None, min_length=1)
    notes: str | None = None
    start_date: date | None = None
    length_weeks: int | None = Field(default=None, ge=1)


class PlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    name: str
    notes: str | None
    start_date: date | None
    length_weeks: int | None
    created_at: datetime
    updated_at: datetime


class PlanDetail(PlanOut):
    sessions: list[SessionOut]
