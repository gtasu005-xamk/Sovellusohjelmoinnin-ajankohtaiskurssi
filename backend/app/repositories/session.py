from datetime import datetime

from sqlalchemy.orm import Session

from app.models.workout_session import WorkoutSession
from app.models.workout_session_item import WorkoutSessionItem


def list_by_user(
    db: Session,
    user_id: int,
    *,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    status: str | None = None,
    activity_type_id: int | None = None,
    unscheduled: bool | None = None,
    plan_id: int | None = None,
) -> list[WorkoutSession]:
    query = db.query(WorkoutSession).filter(WorkoutSession.user_id == user_id)

    if from_date is not None:
        query = query.filter(WorkoutSession.session_at >= from_date)
    if to_date is not None:
        query = query.filter(WorkoutSession.session_at <= to_date)
    if status is not None:
        query = query.filter(WorkoutSession.status == status)
    if activity_type_id is not None:
        query = query.filter(WorkoutSession.items.any(WorkoutSessionItem.activity_type_id == activity_type_id))
    if unscheduled is True:
        query = query.filter(WorkoutSession.session_at.is_(None))
    if unscheduled is False:
        query = query.filter(WorkoutSession.session_at.is_not(None))
    if plan_id is not None:
        query = query.filter(WorkoutSession.plan_id == plan_id)

    return query.order_by(WorkoutSession.session_at.desc().nulls_last(), WorkoutSession.id.desc()).all()


def get_for_user(db: Session, session_id: int, user_id: int) -> WorkoutSession | None:
    return (
        db.query(WorkoutSession)
        .filter(WorkoutSession.id == session_id, WorkoutSession.user_id == user_id)
        .first()
    )


def add(db: Session, session: WorkoutSession) -> WorkoutSession:
    db.add(session)
    db.flush()
    return session


def delete(db: Session, session: WorkoutSession) -> None:
    db.delete(session)
