from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SessionStatus = Literal["planned", "in_progress", "completed"]


class MeasurementIn(BaseModel):
    unit_type_id: int
    planned_value: float | None = None
    actual_value: float | None = None
    set_index: int | None = None

    @model_validator(mode="after")
    def check_values(self):
        if self.planned_value is None and self.actual_value is None:
            raise ValueError("planned_value or actual_value is required")
        return self


class ItemIn(BaseModel):
    activity_type_id: int
    sort_order: int = 0
    notes: str | None = None
    measurements: list[MeasurementIn] = []


class SessionCreate(BaseModel):
    # /docs-esimerkki ilman plan_id:tä (Swaggerin oletus plan_id=0 antaisi 404)
    model_config = ConfigDict(json_schema_extra={"example": {
        "name": "Leg day",
        "session_at": "2026-10-05T17:00:00Z",
        "items": [{"activity_type_id": 1, "measurements": [
            {"unit_type_id": 1, "planned_value": 30}]}],
    }})

    name: str = Field(min_length=1)
    session_at: datetime | None = None
    status: SessionStatus = "planned"
    notes: str | None = None
    intensity: int | None = Field(default=None, ge=1, le=10)
    plan_id: int | None = None
    items: list[ItemIn] = []


# PATCH: vain lähetetyt kentät päivitetään. name/status eivät hyväksy null-arvoa.
# Jos items lähetetään, se korvaa kaikki session itemit.
class SessionUpdate(BaseModel):
    name: str = Field(default=None, min_length=1)
    session_at: datetime | None = None
    status: SessionStatus = None
    notes: str | None = None
    intensity: int | None = Field(default=None, ge=1, le=10)
    plan_id: int | None = None
    items: list[ItemIn] | None = None


class SessionClone(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    session_at: datetime | None = None
    plan_id: int | None = None


class MeasurementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    unit_type_id: int
    planned_value: float | None
    actual_value: float | None
    set_index: int | None


class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    activity_type_id: int
    sort_order: int
    notes: str | None
    measurements: list[MeasurementOut]


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    name: str
    session_at: datetime | None
    status: str
    notes: str | None
    intensity: int | None
    plan_id: int | None
    source_session_id: int | None
    created_at: datetime
    updated_at: datetime
    items: list[ItemOut]
