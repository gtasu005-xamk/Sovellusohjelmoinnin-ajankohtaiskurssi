from datetime import date, datetime, timezone

import pytest

from app.services.analytics import MeasurementInput, SessionInput, build_series, compute_streaks, summarize_sessions

TODAY = date(2026, 10, 20)


def at(year, month, day):
    return datetime(year, month, day, 17, 0, tzinfo=timezone.utc)


def run(duration, distance):
    return [
        MeasurementInput("running", "duration_min", planned_value=30, actual_value=duration),
        MeasurementInput("running", "distance_km", planned_value=5, actual_value=distance),
    ]


def bench(sets):
    measurements = []
    for index, (reps, weight) in enumerate(sets):
        measurements.append(MeasurementInput("bench_press", "reps", 10, reps, set_index=index))
        measurements.append(MeasurementInput("bench_press", "weight_kg", 60, weight, set_index=index))
    return measurements


@pytest.fixture
def sessions():
    return [
        SessionInput(1, at(2026, 10, 5), "completed", 6, run(30, 5.0)),
        SessionInput(2, at(2026, 10, 7), "completed", 8, bench([(10, 60), (8, 60)])),
        SessionInput(3, at(2026, 10, 18), "completed", 7, run(40, 7.5)),
        SessionInput(4, at(2026, 10, 19), "completed", None, bench([(10, 62.5)]) + run(20, 3.0)),
        SessionInput(5, at(2026, 10, 20), "completed", 9, run(25, 4.0)),
        SessionInput(6, at(2026, 9, 28), "completed", 5, run(30, 6.0)),
        SessionInput(7, None, "planned", 10, run(30, 5.0)),
        SessionInput(8, at(2026, 10, 25), "planned", None, run(None, None)),
    ]


def test_summary_empty_list():
    result = summarize_sessions([])
    assert result["session_count"] == 0
    assert result["total_duration_min"] == 0
    assert result["total_distance_km"] == 0
    assert result["avg_intensity"] is None
    assert result["by_activity"] == []


def test_summary_totals(sessions):
    result = summarize_sessions(sessions)
    assert result["session_count"] == 7
    assert result["total_duration_min"] == 30 + 40 + 20 + 25 + 30
    assert result["total_distance_km"] == 5.0 + 7.5 + 3.0 + 4.0 + 6.0
    assert result["avg_intensity"] == round((6 + 8 + 7 + 9 + 5) / 5, 1)


def test_summary_by_activity(sessions):
    result = summarize_sessions(sessions)
    by_activity = {}
    for row in result["by_activity"]:
        by_activity[row["activity_slug"]] = row

    assert by_activity["running"]["session_count"] == 6
    assert by_activity["running"]["distance_km"] == 25.5
    assert by_activity["bench_press"]["session_count"] == 2
    assert by_activity["bench_press"]["distance_km"] == 0


def test_series_empty_list():
    assert build_series([], "sessions", "week") == []


def test_series_sessions_per_week(sessions):
    points = build_series(sessions, "sessions", "week")
    assert points == [
        {"period_label": "2026-W40", "period_start": "2026-09-28", "value": 1},
        {"period_label": "2026-W41", "period_start": "2026-10-05", "value": 2},
        {"period_label": "2026-W42", "period_start": "2026-10-12", "value": 1},
        {"period_label": "2026-W43", "period_start": "2026-10-19", "value": 3},
    ]


def test_series_distance_per_month(sessions):
    points = build_series(sessions, "distance_km", "month")
    assert points == [
        {"period_label": "2026-09", "period_start": "2026-09-01", "value": 6.0},
        {"period_label": "2026-10", "period_start": "2026-10-01", "value": 19.5},
    ]


def test_series_activity_filter(sessions):
    points = build_series(sessions, "sessions", "week", activity_slug="bench_press")
    assert points == [
        {"period_label": "2026-W41", "period_start": "2026-10-05", "value": 1},
        {"period_label": "2026-W43", "period_start": "2026-10-19", "value": 1},
    ]


def test_series_week_crosses_year():
    sessions = [SessionInput(1, at(2025, 12, 29), "completed", None, run(30, 5.0))]
    points = build_series(sessions, "sessions", "week")
    assert points[0]["period_label"] == "2026-W01"
    assert points[0]["period_start"] == "2025-12-29"


def test_series_unknown_metric():
    with pytest.raises(ValueError):
        build_series([], "calories", "week")


def test_streaks_empty_list():
    assert compute_streaks([], TODAY) == {"current_days": 0, "longest_days": 0, "last_active_date": None}


def test_streaks(sessions):
    result = compute_streaks(sessions, TODAY)
    assert result["current_days"] == 3
    assert result["longest_days"] == 3
    assert result["last_active_date"] == "2026-10-20"


def test_streak_continues_from_yesterday(sessions):
    result = compute_streaks(sessions, date(2026, 10, 21))
    assert result["current_days"] == 3


def test_streak_broken_after_gap(sessions):
    result = compute_streaks(sessions, date(2026, 10, 23))
    assert result["current_days"] == 0
    assert result["longest_days"] == 3


def test_streaks_sparse_history():
    sessions = [
        SessionInput(1, at(2026, 1, 5), "completed", None),
        SessionInput(2, at(2026, 3, 1), "completed", None),
    ]
    result = compute_streaks(sessions, TODAY)
    assert result["current_days"] == 0
    assert result["longest_days"] == 1
