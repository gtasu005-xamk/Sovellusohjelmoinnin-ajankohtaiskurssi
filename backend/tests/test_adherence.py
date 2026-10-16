from datetime import datetime, timezone

from app.services.adherence import MeasurementRow, summarize

FROM = datetime(2026, 10, 1, tzinfo=timezone.utc)
TO = datetime(2026, 10, 31, 23, 59, tzinfo=timezone.utc)
IN_RANGE = datetime(2026, 10, 15, 17, 0, tzinfo=timezone.utc)
OUT_OF_RANGE = datetime(2026, 11, 5, 17, 0, tzinfo=timezone.utc)


def test_empty_input():
    result = summarize([], FROM, TO)
    assert result == {"compared": 0, "hit_count": 0, "units": []}


def test_both_values_present():
    rows = [MeasurementRow(unit_type_id=3, planned=10, actual=10, session_at=IN_RANGE)]
    result = summarize(rows, FROM, TO)
    assert result["compared"] == 1
    assert result["hit_count"] == 1
    assert result["units"] == [
        {"unit_type_id": 3, "compared": 1, "planned_total": 10, "actual_total": 10, "hit_count": 1}
    ]


def test_null_values_are_skipped():
    rows = [
        MeasurementRow(unit_type_id=3, planned=10, actual=None, session_at=IN_RANGE),
        MeasurementRow(unit_type_id=3, planned=None, actual=8, session_at=IN_RANGE),
    ]
    result = summarize(rows, FROM, TO)
    assert result["compared"] == 0
    assert result["units"] == []


def test_actual_above_and_below_planned():
    rows = [
        MeasurementRow(unit_type_id=3, planned=10, actual=12, session_at=IN_RANGE),
        MeasurementRow(unit_type_id=3, planned=10, actual=8, session_at=IN_RANGE),
    ]
    result = summarize(rows, FROM, TO)
    assert result["compared"] == 2
    assert result["hit_count"] == 1
    assert result["units"][0]["planned_total"] == 20
    assert result["units"][0]["actual_total"] == 20


def test_session_outside_range_and_unscheduled_are_skipped():
    rows = [
        MeasurementRow(unit_type_id=3, planned=10, actual=10, session_at=OUT_OF_RANGE),
        MeasurementRow(unit_type_id=3, planned=10, actual=10, session_at=None),
    ]
    result = summarize(rows, FROM, TO)
    assert result["compared"] == 0


def test_units_are_not_summed_together():
    rows = [
        MeasurementRow(unit_type_id=2, planned=5, actual=6, session_at=IN_RANGE),
        MeasurementRow(unit_type_id=4, planned=60, actual=55, session_at=IN_RANGE),
    ]
    result = summarize(rows, FROM, TO)
    assert result["compared"] == 2
    assert result["hit_count"] == 1
    assert len(result["units"]) == 2
    assert result["units"][0]["planned_total"] == 5
    assert result["units"][1]["planned_total"] == 60
