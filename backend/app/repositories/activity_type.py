from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.activity_type import ActivityType


def get_system_by_slug(db: Session, slug: str) -> ActivityType | None:
    return (
        db.query(ActivityType)
        .filter(ActivityType.slug == slug, ActivityType.is_system.is_(True))
        .first()
    )


def get_visible(db: Session, activity_type_id: int, user_id: int) -> ActivityType | None:
    return (
        db.query(ActivityType)
        .filter(
            ActivityType.id == activity_type_id,
            or_(ActivityType.user_id.is_(None), ActivityType.user_id == user_id),)
        .first()
    )


def list_visible(db: Session, user_id: int) -> list[ActivityType]:
    return (
        db.query(ActivityType)
        .filter(or_(ActivityType.user_id.is_(None), ActivityType.user_id == user_id))
        .order_by(ActivityType.is_system.desc(), ActivityType.name)
        .all()
    )


def get_by_user_and_slug(db: Session, user_id: int, slug: str) -> ActivityType | None:
    return (
        db.query(ActivityType)
        .filter(ActivityType.user_id == user_id, ActivityType.slug == slug)
        .first()
    )


def add(db: Session, activity: ActivityType) -> ActivityType:
    db.add(activity)
    db.flush()
    return activity


def get_or_create_system(db: Session, *, slug: str, name: str) -> ActivityType:
    activity = get_system_by_slug(db, slug)
    if activity is not None:
        return activity
    activity = ActivityType(slug=slug, name=name, is_system=True, user_id=None)
    db.add(activity)
    db.flush()
    return activity
