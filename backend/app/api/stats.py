from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.stats import Granularity, ProgressMetric, ProgressPoint, StatsSummary
from app.services import stats as stats_service
from app.services.sessions import InvalidRangeError
from app.services.stats import UnknownActivityTypeError

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary", response_model=StatsSummary)
def get_summary(
    from_date: datetime = Query(alias="from"),
    to_date: datetime = Query(alias="to"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return stats_service.get_summary(db, current_user, from_date, to_date)
    except InvalidRangeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="'from' must be before 'to'")


@router.get("/progress", response_model=list[ProgressPoint])
def get_progress(
    from_date: datetime = Query(alias="from"),
    to_date: datetime = Query(alias="to"),
    metric: ProgressMetric = "sessions",
    granularity: Granularity = "week",
    activity_type_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """metric: sessions (määrä), duration_min tai distance_km (actual-arvoista, samat nimet kuin yksikön slug).
    granularity: week (ISO-viikko, alkaa maanantaina) tai month."""
    try:
        return stats_service.get_progress(db, current_user, from_date, to_date, metric, granularity, activity_type_id)
    except InvalidRangeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="'from' must be before 'to'")
    except UnknownActivityTypeError:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unknown activity_type_id")
