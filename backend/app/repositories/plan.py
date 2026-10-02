from sqlalchemy.orm import Session

from app.models.workout_plan import WorkoutPlan


def get_for_user(db: Session, plan_id: int, user_id: int) -> WorkoutPlan | None:
    return (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.id == plan_id, WorkoutPlan.user_id == user_id)
        .first()
    )
