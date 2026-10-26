from pydantic import BaseModel

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
