from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.models.user import User
from app.repositories import activity_type as activity_type_repo
from app.repositories import goal as goal_repo
from app.repositories import unit_type as unit_type_repo
from app.schemas.goal import GoalCreate, GoalUpdate


class GoalNotFoundError(Exception):
    pass


class InvalidGoalError(Exception):
    pass


def _check_catalog(db: Session, user: User, unit_type_id: int, activity_type_id: int | None) -> None:
    if unit_type_repo.get_by_id(db, unit_type_id) is None:
        raise InvalidGoalError(f"Unknown unit_type_id {unit_type_id}")
    if activity_type_id is not None:
        if activity_type_repo.get_visible(db, activity_type_id, user.id) is None:
            raise InvalidGoalError(f"Unknown activity_type_id {activity_type_id}")


def list_goals(db: Session, user: User, active: bool | None = None) -> list[Goal]:
    return goal_repo.list_by_user(db, user.id, active)


def get_goal(db: Session, user: User, goal_id: int) -> Goal:
    goal = goal_repo.get_for_user(db, goal_id, user.id)
    if goal is None:
        raise GoalNotFoundError()
    return goal


def create_goal(db: Session, user: User, data: GoalCreate) -> Goal:
    _check_catalog(db, user, data.unit_type_id, data.activity_type_id)
    goal = Goal(
        user_id=user.id,
        unit_type_id=data.unit_type_id,
        activity_type_id=data.activity_type_id,
        target_value=data.target_value,
        period=data.period,
        active=data.active,
    )
    goal_repo.add(db, goal)
    db.commit()
    db.refresh(goal)
    return goal


def update_goal(db: Session, user: User, goal_id: int, data: GoalUpdate) -> Goal:
    goal = get_goal(db, user, goal_id)
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(goal, field, value)
    _check_catalog(db, user, goal.unit_type_id, goal.activity_type_id)
    db.commit()
    db.refresh(goal)
    return goal


def delete_goal(db: Session, user: User, goal_id: int) -> None:
    goal = get_goal(db, user, goal_id)
    goal_repo.delete(db, goal)
    db.commit()
