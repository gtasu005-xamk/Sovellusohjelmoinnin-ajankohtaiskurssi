from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalOut, GoalUpdate
from app.services import goals as goal_service
from app.services.goals import GoalNotFoundError, InvalidGoalError

router = APIRouter(prefix="/goals", tags=["goals"])


def _not_found() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goal not found")


def _invalid(error: Exception) -> HTTPException:
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))


@router.get("", response_model=list[GoalOut])
def list_goals(active: bool | None = None, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return goal_service.list_goals(db, current_user, active)


@router.post("", response_model=GoalOut, status_code=status.HTTP_201_CREATED)
def create_goal(body: GoalCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    try:
        return goal_service.create_goal(db, current_user, body)
    except InvalidGoalError as e:
        raise _invalid(e)


@router.get("/{goal_id}", response_model=GoalOut)
def get_goal(goal_id: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    try:
        return goal_service.get_goal(db, current_user, goal_id)
    except GoalNotFoundError:
        raise _not_found()


@router.patch("/{goal_id}", response_model=GoalOut)
def update_goal(goal_id: int, body: GoalUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    try:
        return goal_service.update_goal(db, current_user, goal_id, body)
    except GoalNotFoundError:
        raise _not_found()
    except InvalidGoalError as e:
        raise _invalid(e)


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(goal_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    try:
        goal_service.delete_goal(db, current_user, goal_id)
    except GoalNotFoundError:
        raise _not_found()
