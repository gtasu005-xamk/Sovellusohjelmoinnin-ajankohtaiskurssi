from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.stats import (GoalProgress, Granularity, ProgressMetric, ProgressPoint, StatsCompare, StatsSummary,
                               StreakResponse)
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


@router.get("/export")
def export_csv(
    from_date: datetime = Query(alias="from"),
    to_date: datetime = Query(alias="to"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Summary CSV:nä valitulta jaksolta. Rivi per aktiviteetti + total-rivi."""
    try:
        content = stats_service.export_summary_csv(db, current_user, from_date, to_date)
    except InvalidRangeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="'from' must be before 'to'")
    filename = f"stats_{from_date.date()}_{to_date.date()}.csv"
    return Response(content=content, media_type="text/csv",
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.get("/compare", response_model=StatsCompare)
def get_compare(
    from_date: datetime = Query(alias="from"),
    to_date: datetime = Query(alias="to"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Valittu jakso vs. edellinen yhtä pitkä jakso juuri ennen sitä. delta = current - previous."""
    try:
        return stats_service.get_compare(db, current_user, from_date, to_date)
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


@router.get("/streaks", response_model=StreakResponse)
def get_streaks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Putket koko historiasta. Putki = peräkkäiset päivät (UTC) joina vähintään yksi sessio.
    Ajastamattomat ja tulevat sessiot ei lasketa. Nykyinen putki jatkuu jos eilen oli sessio,
    vaikka tänään ei vielä olisi."""
    return stats_service.get_streaks(db, current_user)


@router.get("/goals", response_model=list[GoalProgress])
def get_goal_progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Aktiivisten tavoitteiden toteutuma kuluvalta viikolta tai kuukaudelta (UTC).
    total = tavoitteen yksikön actual-arvojen summa, percent = total / target_value * 100 (voi olla yli 100)."""
    return stats_service.get_goal_progress(db, current_user)
