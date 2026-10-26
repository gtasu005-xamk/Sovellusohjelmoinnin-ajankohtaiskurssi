from datetime import datetime
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workout_session import WorkoutSession
from app.repositories import session as session_repo
from app.services.analytics import MeasurementInput, SessionInput, summarize_sessions
from app.services.sessions import InvalidRangeError


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
