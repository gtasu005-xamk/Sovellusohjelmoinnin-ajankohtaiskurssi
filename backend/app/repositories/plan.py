from sqlalchemy.orm import Session

from app.models.workout_plan import WorkoutPlan


def list_by_user(db: Session, user_id: int) -> list[WorkoutPlan]:
    return (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user_id)
        .order_by(WorkoutPlan.created_at.desc())
        .all()
    )


def get_for_user(db: Session, plan_id: int, user_id: int) -> WorkoutPlan | None:
    return (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.id == plan_id, WorkoutPlan.user_id == user_id)
        .first()
    )


def add(db: Session, plan: WorkoutPlan) -> WorkoutPlan:
    db.add(plan)
    db.flush()
    return plan


def delete(db: Session, plan: WorkoutPlan) -> None:
    db.delete(plan)
