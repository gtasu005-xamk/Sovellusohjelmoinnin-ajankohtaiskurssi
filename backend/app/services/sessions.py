from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workout_session import WorkoutSession
from app.models.workout_session_item import WorkoutSessionItem
from app.models.workout_session_measurement import WorkoutSessionMeasurement
from app.repositories import plan as plan_repo
from app.repositories import session as session_repo
from app.schemas.session import ItemIn, SessionCreate, SessionUpdate


class SessionNotFoundError(Exception):
    pass


class PlanNotFoundError(Exception):
    pass


def _check_plan(db: Session, user: User, plan_id: int | None) -> None:
    if plan_id is not None and plan_repo.get_for_user(db, plan_id, user.id) is None:
        raise PlanNotFoundError()


def _build_items(items: list[ItemIn]) -> list[WorkoutSessionItem]:
    return [
        WorkoutSessionItem(
            activity_type_id=item.activity_type_id,
            sort_order=item.sort_order,
            notes=item.notes,
            measurements=[WorkoutSessionMeasurement(**m.model_dump()) for m in item.measurements],
        )
        for item in items
    ]


def list_sessions(db: Session, user: User) -> list[WorkoutSession]:
    return session_repo.list_by_user(db, user.id)


# Toisen käyttäjän sessio näyttää samalta kuin olematon: 404.
def get_session(db: Session, user: User, session_id: int) -> WorkoutSession:
    session = session_repo.get_for_user(db, session_id, user.id)
    if session is None:
        raise SessionNotFoundError()
    return session


def create_session(db: Session, user: User, data: SessionCreate) -> WorkoutSession:
    _check_plan(db, user, data.plan_id)
    session = WorkoutSession(
        user_id=user.id,
        **data.model_dump(exclude={"items"}),
        items=_build_items(data.items),
    )
    session_repo.add(db, session)
    db.commit()
    db.refresh(session)
    return session


def update_session(db: Session, user: User, session_id: int, data: SessionUpdate) -> WorkoutSession:
    session = get_session(db, user, session_id)
    changes = data.model_dump(exclude_unset=True, exclude={"items"})
    if "plan_id" in changes:
        _check_plan(db, user, changes["plan_id"])
    for field, value in changes.items():
        setattr(session, field, value)
    if data.items is not None:
        session.items = _build_items(data.items)
    db.commit()
    db.refresh(session)
    return session


def delete_session(db: Session, user: User, session_id: int) -> None:
    session = get_session(db, user, session_id)
    session_repo.delete(db, session)
    db.commit()
