from sqlalchemy.orm import Session
from app.models.activity_type import ActivityType


def get_system_by_slug(db: Session, slug: str) -> ActivityType | None:
    return (
        db.query(ActivityType)
        .filter(ActivityType.slug == slug, ActivityType.is_system.is_(True))
        .first()
    )


def get_or_create_system(db: Session, *, slug: str, name: str) -> ActivityType:
    activity = get_system_by_slug(db, slug)
    if activity is not None:
        return activity
    activity = ActivityType(slug=slug, name=name, is_system=True, user_id=None)
    db.add(activity)
    db.flush()
    return activity
