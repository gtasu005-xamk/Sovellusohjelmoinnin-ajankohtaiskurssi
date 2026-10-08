from sqlalchemy.orm import Session

from app.models.activity_type import ActivityType
from app.models.activity_type_unit_type import ActivityTypeUnitType
from app.models.user import User
from app.repositories import activity_type as activity_type_repo
from app.repositories import unit_type as unit_type_repo
from app.schemas.activity_type import ActivityTypeCreate


class DuplicateSlugError(Exception):
    pass


class InvalidUnitTypeError(Exception):
    pass


def list_activity_types(db: Session, user: User) -> list[ActivityType]:
    return activity_type_repo.list_visible(db, user.id)


def create_activity_type(db: Session, user: User, data: ActivityTypeCreate) -> ActivityType:
    if activity_type_repo.get_by_user_and_slug(db, user.id, data.slug) is not None:
        raise DuplicateSlugError()

    activity = ActivityType(name=data.name, slug=data.slug, user_id=user.id, is_system=False)

    used_units = []
    for link in data.unit_links:
        if unit_type_repo.get_by_id(db, link.unit_type_id) is None:
            raise InvalidUnitTypeError(f"Unknown unit_type_id {link.unit_type_id}")
        if link.unit_type_id in used_units:
            raise InvalidUnitTypeError(f"unit_type_id {link.unit_type_id} is listed twice")
        used_units.append(link.unit_type_id)

        activity.unit_links.append(ActivityTypeUnitType(
            unit_type_id=link.unit_type_id,
            sort_order=link.sort_order,
            is_required=link.is_required,
            per_set=link.per_set,
        ))

    activity_type_repo.add(db, activity)
    db.commit()
    db.refresh(activity)
    return activity
