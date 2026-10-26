from datetime import datetime

from sqlalchemy.orm import Session

from app.models.workout_session import WorkoutSession
from app.models.workout_session_item import WorkoutSessionItem
from app.models.workout_session_measurement import WorkoutSessionMeasurement


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
    page: int = 1,
    limit: int | None = None,
) -> tuple[list[WorkoutSession], int]:
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

    total = query.count()
    query = query.order_by(WorkoutSession.session_at.desc().nulls_last(), WorkoutSession.id.desc())
    if limit is not None:
        query = query.offset((page - 1) * limit).limit(limit)
    return query.all(), total


def list_for_calendar(
    db: Session,
    user_id: int,
    from_date: datetime,
    to_date: datetime,
    plan_id: int | None = None,
) -> list[WorkoutSession]:
    query = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == user_id,
        WorkoutSession.session_at.is_not(None),
        WorkoutSession.session_at >= from_date,
        WorkoutSession.session_at <= to_date,
    )
    if plan_id is not None:
        query = query.filter(WorkoutSession.plan_id == plan_id)
    return query.order_by(WorkoutSession.session_at, WorkoutSession.id).all()


def list_dated_by_user(db: Session, user_id: int) -> list[WorkoutSession]:
    return (
        db.query(WorkoutSession)
        .filter(WorkoutSession.user_id == user_id, WorkoutSession.session_at.is_not(None))
        .order_by(WorkoutSession.session_at)
        .all()
    )


def list_measurements_for_user(db: Session, user_id: int, from_date: datetime, to_date: datetime) -> list:
    return (
        db.query(WorkoutSessionMeasurement, WorkoutSession.session_at)
        .join(WorkoutSessionItem, WorkoutSessionMeasurement.session_item_id == WorkoutSessionItem.id)
        .join(WorkoutSession, WorkoutSessionItem.session_id == WorkoutSession.id)
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSession.session_at.is_not(None),
            WorkoutSession.session_at >= from_date,
            WorkoutSession.session_at <= to_date,
        )
        .all()
    )


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
