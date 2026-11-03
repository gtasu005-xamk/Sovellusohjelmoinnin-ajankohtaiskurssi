from datetime import datetime
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


class StatsDelta(BaseModel):
    session_count: int
    total_duration_min: float
    total_distance_km: float


class StatsCompare(BaseModel):
    previous_from: datetime
    previous_to: datetime
    current: StatsSummary
    previous: StatsSummary
    delta: StatsDelta


ProgressMetric = Literal["sessions", "duration_min", "distance_km"]
Granularity = Literal["week", "month"]

class ProgressPoint(BaseModel):
    period_label: str
    period_start: str
    value: float


class StreakResponse(BaseModel):
    current_days: int
    longest_days: int
    last_active_date: str | None


class GoalProgress(BaseModel):
    goal_id: int
    unit_type_id: int
    unit_name: str
    activity_type_id: int | None
    activity_name: str | None
    period: str
    period_start: datetime
    period_end: datetime
    target_value: float
    total: float
    percent: float
