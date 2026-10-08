from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CalendarEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    session_at: datetime
    status: str
    plan_id: int | None
    source_session_id: int | None
