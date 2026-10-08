from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.plan import PlanCreate, PlanDetail, PlanOut, PlanUpdate
from app.services import plans as plan_service
from app.services.plans import PlanNotFoundError
from app.services.sessions import SessionNotFoundError

router = APIRouter(prefix="/plans", tags=["plans"])


def _not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


@router.get("", response_model=list[PlanOut])
def list_plans(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return plan_service.list_plans(db, current_user)


@router.post("", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
def create_plan(body: PlanCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return plan_service.create_plan(db, current_user, body)


@router.get("/{plan_id}", response_model=PlanDetail)
def get_plan(plan_id: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    try:
        return plan_service.get_plan(db, current_user, plan_id)
    except PlanNotFoundError:
        raise _not_found("Plan not found")


@router.patch("/{plan_id}", response_model=PlanOut)
def update_plan(plan_id: int, body: PlanUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    try:
        return plan_service.update_plan(db, current_user, plan_id, body)
    except PlanNotFoundError:
        raise _not_found("Plan not found")


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    try:
        plan_service.delete_plan(db, current_user, plan_id)
    except PlanNotFoundError:
        raise _not_found("Plan not found")


@router.post("/{plan_id}/sessions/{session_id}", response_model=PlanDetail)
def attach_session(plan_id: int, session_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    try:
        return plan_service.attach_session(db, current_user, plan_id, session_id)
    except PlanNotFoundError:
        raise _not_found("Plan not found")
    except SessionNotFoundError:
        raise _not_found("Session not found")


@router.delete("/{plan_id}/sessions/{session_id}", response_model=PlanDetail)
def detach_session(plan_id: int, session_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    try:
        return plan_service.detach_session(db, current_user, plan_id, session_id)
    except PlanNotFoundError:
        raise _not_found("Plan not found")
    except SessionNotFoundError:
        raise _not_found("Session not found")
