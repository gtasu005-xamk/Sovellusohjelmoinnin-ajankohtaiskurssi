from sqlalchemy.orm import Session
from app.models.activity_type_unit_type import ActivityTypeUnitType
from app.repositories import activity_type as activity_type_repo
from app.repositories import unit_type as unit_type_repo

UNIT_TYPES = [
    {"slug": "duration_min", "name": "Duration (min)"},
    {"slug": "distance_km", "name": "Distance (km)"},
    {"slug": "reps", "name": "Reps"},
    {"slug": "weight_kg", "name": "Weight (kg)"},
]

CARDIO_ACTIVITIES = [
    {"slug": "running", "name": "Running"},
    {"slug": "cycling", "name": "Cycling"},
]

STRENGTH_ACTIVITIES = [
    {"slug": "bench_press", "name": "Bench press"},
    {"slug": "barbell_curl", "name": "Barbell curl"},
    {"slug": "hammer_curl", "name": "Hammer curl"},
    {"slug": "incline_curl", "name": "Incline curl"},
    {"slug": "face_pull", "name": "Face pull"},
]

OTHER_ACTIVITIES = [{"slug": "other", "name": "Other"}]


def _link(db: Session, *, activity_id: int, unit_id: int, per_set: bool, sort_order: int) -> None:
    existing = (
        db.query(ActivityTypeUnitType)
        .filter_by(activity_type_id=activity_id, unit_type_id=unit_id)
        .first()
    )
    if existing is not None:
        return
    db.add(
        ActivityTypeUnitType(
            activity_type_id=activity_id,
            unit_type_id=unit_id,
            per_set=per_set,
            sort_order=sort_order,
        )
    )


def seed_catalog(db: Session) -> None:
    units = {u["slug"]: unit_type_repo.get_or_create(db, **u) for u in UNIT_TYPES}

    for entry in CARDIO_ACTIVITIES:
        activity = activity_type_repo.get_or_create_system(db, **entry)
        _link(db, activity_id=activity.id, unit_id=units["duration_min"].id, per_set=False, sort_order=0)
        _link(db, activity_id=activity.id, unit_id=units["distance_km"].id, per_set=False, sort_order=1)

    for entry in STRENGTH_ACTIVITIES:
        activity = activity_type_repo.get_or_create_system(db, **entry)
        _link(db, activity_id=activity.id, unit_id=units["reps"].id, per_set=True, sort_order=0)
        _link(db, activity_id=activity.id, unit_id=units["weight_kg"].id, per_set=True, sort_order=1)

    for entry in OTHER_ACTIVITIES:
        activity = activity_type_repo.get_or_create_system(db, **entry)
        _link(db, activity_id=activity.id, unit_id=units["duration_min"].id, per_set=False, sort_order=0)

    db.commit()
