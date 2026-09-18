from sqlalchemy.orm import Session
from app.models.unit_type import UnitType


def get_by_slug(db: Session, slug: str) -> UnitType | None:
    return db.query(UnitType).filter(UnitType.slug == slug).first()


def get_or_create(db: Session, *, slug: str, name: str, is_system: bool = True) -> UnitType:
    unit = get_by_slug(db, slug)
    if unit is not None:
        return unit
    unit = UnitType(slug=slug, name=name, is_system=is_system)
    db.add(unit)
    db.flush()
    return unit
