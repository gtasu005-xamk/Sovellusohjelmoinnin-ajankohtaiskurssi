from dataclasses import dataclass
from datetime import datetime


@dataclass
class MeasurementRow:
    unit_type_id: int
    planned: float | None
    actual: float | None
    session_at: datetime | None


def summarize(rows: list[MeasurementRow], from_date: datetime, to_date: datetime) -> dict:
    compared = 0
    hit_count = 0
    units = {}

    for row in rows:
        if row.session_at is None:
            continue
        if row.session_at < from_date or row.session_at > to_date:
            continue
        if row.planned is None or row.actual is None:
            continue

        compared += 1
        hit = row.actual >= row.planned
        if hit:
            hit_count += 1

        if row.unit_type_id not in units:
            units[row.unit_type_id] = {
                "unit_type_id": row.unit_type_id,
                "compared": 0,
                "planned_total": 0.0,
                "actual_total": 0.0,
                "hit_count": 0,
            }
        unit = units[row.unit_type_id]
        unit["compared"] += 1
        unit["planned_total"] += row.planned
        unit["actual_total"] += row.actual
        if hit:
            unit["hit_count"] += 1

    return {
        "compared": compared,
        "hit_count": hit_count,
        "units": list(units.values()),
    }
