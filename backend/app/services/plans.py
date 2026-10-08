from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workout_plan import WorkoutPlan
from app.repositories import plan as plan_repo
from app.schemas.plan import PlanCreate, PlanUpdate
from app.services.sessions import SessionNotFoundError, get_session


class PlanNotFoundError(Exception):
    pass


def list_plans(db: Session, user: User) -> list[WorkoutPlan]:
    return plan_repo.list_by_user(db, user.id)


def get_plan(db: Session, user: User, plan_id: int) -> WorkoutPlan:
    plan = plan_repo.get_for_user(db, plan_id, user.id)
    if plan is None:
        raise PlanNotFoundError()
    return plan


def create_plan(db: Session, user: User, data: PlanCreate) -> WorkoutPlan:
    plan = WorkoutPlan(
        user_id=user.id,
        name=data.name,
        notes=data.notes,
        start_date=data.start_date,
        length_weeks=data.length_weeks,
    )
    plan_repo.add(db, plan)
    db.commit()
    db.refresh(plan)
    return plan


def update_plan(db: Session, user: User, plan_id: int, data: PlanUpdate) -> WorkoutPlan:
    plan = get_plan(db, user, plan_id)
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(plan, field, value)
    db.commit()
    db.refresh(plan)
    return plan


def delete_plan(db: Session, user: User, plan_id: int) -> None:
    plan = get_plan(db, user, plan_id)
    plan_repo.delete(db, plan)
    db.commit()


def attach_session(db: Session, user: User, plan_id: int, session_id: int) -> WorkoutPlan:
    plan = get_plan(db, user, plan_id)
    session = get_session(db, user, session_id)
    session.plan_id = plan.id
    db.commit()
    db.refresh(plan)
    return plan


def detach_session(db: Session, user: User, plan_id: int, session_id: int) -> WorkoutPlan:
    plan = get_plan(db, user, plan_id)
    session = get_session(db, user, session_id)
    if session.plan_id != plan.id:
        raise SessionNotFoundError()
    session.plan_id = None
    db.commit()
    db.refresh(plan)
    return plan
