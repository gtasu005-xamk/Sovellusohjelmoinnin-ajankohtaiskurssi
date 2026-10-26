from pydantic import BaseModel
from typing import Literal

class ActivitySummary(BaseModel):
    activity_slug: str
    session_count: int
    duration_min: float
    distance_km: float


class StatsSummary(BaseModel):
    session_count: int
    total_duration_min: float
    total_distance_km: float
    avg_intensity: float | None
    by_activity: list[ActivitySummary]


ProgressMetric = Literal["sessions", "duration_min", "distance_km"]
Granularity = Literal["week", "month"]

class ProgressPoint(BaseModel):
    period_label: str
    period_start: str
    value: float
