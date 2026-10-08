from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.calendar import CalendarEntry
from app.services import calendar as calendar_service
from app.services.sessions import InvalidRangeError

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("", response_model=list[CalendarEntry])
def get_calendar(
    from_date: datetime = Query(alias="from"),
    to_date: datetime = Query(alias="to"),
    plan_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return calendar_service.get_calendar(db, current_user, from_date, to_date, plan_id)
    except InvalidRangeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="'from' must be before 'to'")
