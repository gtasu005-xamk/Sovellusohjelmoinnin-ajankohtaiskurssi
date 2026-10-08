from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.activity_type import ActivityTypeCreate, ActivityTypeOut
from app.services import activity_types as activity_type_service
from app.services.activity_types import DuplicateSlugError, InvalidUnitTypeError

router = APIRouter(prefix="/activity-types", tags=["activity-types"])


@router.get("", response_model=list[ActivityTypeOut])
def list_activity_types(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return activity_type_service.list_activity_types(db, current_user)


@router.post("", response_model=ActivityTypeOut, status_code=status.HTTP_201_CREATED)
def create_activity_type(body: ActivityTypeCreate, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    try:
        return activity_type_service.create_activity_type(db, current_user, body)
    except DuplicateSlugError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug already in use")
    except InvalidUnitTypeError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
