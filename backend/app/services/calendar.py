from datetime import datetime

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workout_session import WorkoutSession
from app.repositories import session as session_repo
from app.services.sessions import InvalidRangeError


def get_calendar(
    db: Session,
    user: User,
    from_date: datetime,
    to_date: datetime,
    plan_id: int | None = None,
) -> list[WorkoutSession]:
    if from_date > to_date:
        raise InvalidRangeError()
    return session_repo.list_for_calendar(db, user.id, from_date, to_date, plan_id)
