from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workout_session import WorkoutSession
from app.repositories import session as session_repo
from app.services.analytics import MeasurementInput, SessionInput, build_series, compute_streaks, summarize_sessions
from app.services.sessions import InvalidRangeError
from app.repositories import activity_type as activity_type_repo

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
