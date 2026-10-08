from sqlalchemy.orm import Session

from app.models.goal import Goal


def list_by_user(db: Session, user_id: int, active: bool | None = None) -> list[Goal]:
    query = db.query(Goal).filter(Goal.user_id == user_id)
    if active is not None:
        query = query.filter(Goal.active == active)
    return query.order_by(Goal.created_at.desc()).all()


def get_for_user(db: Session, goal_id: int, user_id: int) -> Goal | None:
    return db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == user_id).first()


def add(db: Session, goal: Goal) -> Goal:
    db.add(goal)
    db.flush()
    return goal


def delete(db: Session, goal: Goal) -> None:
    db.delete(goal)
