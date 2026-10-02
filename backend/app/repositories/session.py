from sqlalchemy.orm import Session

from app.models.workout_session import WorkoutSession


def list_by_user(db: Session, user_id: int) -> list[WorkoutSession]:
    return (
        db.query(WorkoutSession)
        .filter(WorkoutSession.user_id == user_id)
        .order_by(WorkoutSession.session_at.desc().nulls_last(), WorkoutSession.id.desc())
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
