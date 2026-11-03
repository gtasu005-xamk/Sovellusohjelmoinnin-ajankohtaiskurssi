import csv
import io
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workout_session import WorkoutSession
from app.repositories import session as session_repo
from app.services.analytics import (MeasurementInput, SessionInput, build_series, compute_streaks,
                                    goal_completion, goal_period_range, previous_window, summarize_sessions)
from app.services.sessions import InvalidRangeError
from app.repositories import activity_type as activity_type_repo
from app.repositories import goal as goal_repo

class UnknownActivityTypeError(Exception):
    pass


def to_session_input(session: WorkoutSession) -> SessionInput:
    measurements = []
    for item in session.items:
        for m in item.measurements:
            measurements.append(MeasurementInput(
                activity_slug=item.activity_type.slug,
                unit_slug=m.unit_type.slug,
                planned_value=m.planned_value,
                actual_value=m.actual_value,
                set_index=m.set_index,
            ))
    return SessionInput(
        session_id=session.id,
        session_at=session.session_at,
        status=session.status,
        intensity=session.intensity,
        measurements=measurements,
    )


def load_sessions(db: Session, user: User, from_date: datetime, to_date: datetime) -> list[SessionInput]:
    if from_date > to_date:
        raise InvalidRangeError()

    sessions = []
    for session in session_repo.list_for_calendar(db, user.id, from_date, to_date):
        sessions.append(to_session_input(session))
    return sessions


def get_summary(db: Session, user: User, from_date: datetime, to_date: datetime) -> dict:
    sessions = load_sessions(db, user, from_date, to_date)
    return summarize_sessions(sessions)


def export_summary_csv(db: Session, user: User, from_date: datetime, to_date: datetime) -> str:
    summary = get_summary(db, user, from_date, to_date)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["activity_slug", "session_count", "duration_min", "distance_km"])
    for row in summary["by_activity"]:
        writer.writerow([row["activity_slug"], row["session_count"], row["duration_min"], row["distance_km"]])
    writer.writerow(["total", summary["session_count"], summary["total_duration_min"], summary["total_distance_km"]])
    return output.getvalue()


def get_compare(db: Session, user: User, from_date: datetime, to_date: datetime) -> dict:
    current = get_summary(db, user, from_date, to_date)
    previous_from, previous_to = previous_window(from_date, to_date)
    previous = get_summary(db, user, previous_from, previous_to)
    return {
        "previous_from": previous_from,
        "previous_to": previous_to,
        "current": current,
        "previous": previous,
        "delta": {
            "session_count": current["session_count"] - previous["session_count"],
            "total_duration_min": current["total_duration_min"] - previous["total_duration_min"],
            "total_distance_km": current["total_distance_km"] - previous["total_distance_km"],
        },
    }


def get_progress(db: Session, user: User, from_date: datetime, to_date: datetime,
                 metric: str, granularity: str, activity_type_id: int | None = None) -> list[dict]:
    activity_slug = None
    if activity_type_id is not None:
        activity = activity_type_repo.get_visible(db, activity_type_id, user.id)
        if activity is None:
            raise UnknownActivityTypeError()
        activity_slug = activity.slug

    sessions = load_sessions(db, user, from_date, to_date)
    return build_series(sessions, metric, granularity, activity_slug)


def get_streaks(db: Session, user: User) -> dict:
    sessions = []
    for session in session_repo.list_dated_by_user(db, user.id):
        sessions.append(to_session_input(session))
    today = datetime.now(timezone.utc).date()
    return compute_streaks(sessions, today)


def get_goal_progress(db: Session, user: User) -> list[dict]:
    today = datetime.now(timezone.utc).date()
    results = []
    for goal in goal_repo.list_by_user(db, user.id, active=True):
        start, end = goal_period_range(goal.period, today)
        sessions = load_sessions(db, user, start, end)

        activity_slug = None
        activity_name = None
        if goal.activity_type is not None:
            activity_slug = goal.activity_type.slug
            activity_name = goal.activity_type.name

        completion = goal_completion(sessions, goal.unit_type.slug, goal.target_value, activity_slug)
        results.append({
            "goal_id": goal.id,
            "unit_type_id": goal.unit_type_id,
            "unit_name": goal.unit_type.name,
            "activity_type_id": goal.activity_type_id,
            "activity_name": activity_name,
            "period": goal.period,
            "period_start": start,
            "period_end": end,
            "target_value": goal.target_value,
            "total": completion["total"],
            "percent": completion["percent"],
        })
    return results
