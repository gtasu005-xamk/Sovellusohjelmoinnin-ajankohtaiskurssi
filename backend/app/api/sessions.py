from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.session import AdherenceSummary, SessionClone, SessionCreate, SessionOut, SessionPage, SessionStatus, SessionUpdate
from app.services import sessions as session_service
from app.services.sessions import (InvalidMeasurementError, InvalidRangeError, PlanNotFoundError, SessionNotFoundError,)

router = APIRouter(prefix="/sessions", tags=["sessions"])


def _not_found(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def _invalid(error: Exception) -> HTTPException:
    return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))


@router.get("", response_model=SessionPage)
def list_sessions(
    from_date: datetime | None = Query(None, alias="from"),
    to_date: datetime | None = Query(None, alias="to"),
    session_status: SessionStatus | None = Query(None, alias="status"),
    activity_type_id: int | None = None,
    unscheduled: bool | None = None,
    plan_id: int | None = None,
    page: int = Query(1, ge=1),
    limit: int | None = Query(None, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return session_service.list_sessions(
            db,
            current_user,
            from_date=from_date,
            to_date=to_date,
            status=session_status,
            activity_type_id=activity_type_id,
            unscheduled=unscheduled,
            plan_id=plan_id,
            page=page,
            limit=limit,
        )
    except InvalidRangeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="'from' must be before 'to'")


@router.get("/adherence", response_model=AdherenceSummary)
def get_adherence(
    from_date: datetime = Query(alias="from"),
    to_date: datetime = Query(alias="to"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Planned vs actual -esikatselu Sprint 4:ää varten. Vertaa vain mittauksia, joissa on molemmat arvot, ryhmiteltynä yksikön mukaan."""
    try:
        return session_service.get_adherence(db, current_user, from_date, to_date)
    except InvalidRangeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="'from' must be before 'to'")


@router.post("", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_session(body: SessionCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    try:
        return session_service.create_session(db, current_user, body)
    except PlanNotFoundError:
        raise _not_found("Plan not found")
    except InvalidMeasurementError as e:
        raise _invalid(e)


@router.get("/{session_id}", response_model=SessionOut)
def get_session(session_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    try:
        return session_service.get_session(db, current_user, session_id)
    except SessionNotFoundError:
        raise _not_found("Session not found")


@router.patch("/{session_id}", response_model=SessionOut)
def update_session(session_id: int, body: SessionUpdate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    try:
        return session_service.update_session(db, current_user, session_id, body)
    except SessionNotFoundError:
        raise _not_found("Session not found")
    except PlanNotFoundError:
        raise _not_found("Plan not found")
    except InvalidMeasurementError as e:
        raise _invalid(e)


@router.post("/{session_id}/clone", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def clone_session(session_id: int, body: SessionClone | None = None, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    if body is None:
        body = SessionClone()
    try:
        return session_service.clone_session(db, current_user, session_id, body)
    except SessionNotFoundError:
        raise _not_found("Session not found")
    except PlanNotFoundError:
        raise _not_found("Plan not found")


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    try:
        session_service.delete_session(db, current_user, session_id)
    except SessionNotFoundError:
        raise _not_found("Session not found")
