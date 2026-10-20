## Analytiikka: pelkkiä laskufunktioita, ei I/O:ta.
## Ei hae tietokannasta eikä importtaa FastAPI:a tai SQLAlchemya, jotta testit toimii ilman kantaa.
## Kutsuja lataa yhden käyttäjän sessiot, rajaa ne valmiiksi
## kirjautuneeseen käyttäjään ja antaa ne tänne SessionInput-listana.
##
## SessionInput = yksi sessio (aika, status, intensiteetti ja mittaukset)
## MeasurementInput = yksi mittaus, aktiviteetti ja yksikkö sluggina (esim. running, distance_km)
## planned/actual voi olla None jos arvoa ei ole syötetty

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

@dataclass
class MeasurementInput:
    activity_slug: str
    unit_slug: str
    planned_value: float | None
    actual_value: float | None
    set_index: int | None = None

@dataclass
class SessionInput:
    session_id: int
    session_at: datetime | None
    status: str
    intensity: int | None
    measurements: list[MeasurementInput] = field(default_factory=list)


## Yhteenveto. Vain sessiot joilla on päivämäärä otetaan mukaan.
## Kesto ja matka lasketaan actual-arvoista, puuttuva = 0, plannedia ei käytetä.
## avg_intensity on None jos intensiteettejä ei ole ollenkaan (esim. tyhjä lista).
def summarize_sessions(sessions: list[SessionInput]) -> dict:
    session_count = 0
    total_duration = 0.0
    total_distance = 0.0
    intensities = []
    by_activity = {}

    for session in sessions:
        if session.session_at is None:
            continue
        session_count += 1
        if session.intensity is not None:
            intensities.append(session.intensity)

        activities_in_session = []
        for m in session.measurements:
            if m.activity_slug not in by_activity:
                by_activity[m.activity_slug] = {
                "activity_slug": m.activity_slug,
                "session_count": 0,
                "duration_min": 0.0,
                "distance_km": 0.0,
                }
            activity = by_activity[m.activity_slug]

            if m.activity_slug not in activities_in_session:
                activities_in_session.append(m.activity_slug)
                activity["session_count"] += 1

            if m.actual_value is None:
                continue
            if m.unit_slug == "duration_min":
                total_duration += m.actual_value
                activity["duration_min"] += m.actual_value
            if m.unit_slug == "distance_km":
                total_distance += m.actual_value
                activity["distance_km"] += m.actual_value

    avg_intensity = None
    if len(intensities) > 0:
        avg_intensity = round(sum(intensities) / len(intensities), 1)

    return {
        "session_count": session_count,
        "total_duration_min": total_duration,
        "total_distance_km": total_distance,
        "avg_intensity": avg_intensity,
        "by_activity": list(by_activity.values()),
    }


## Aikasarja viikoittain tai kuukausittain. Viikko alkaa maanantaina (ISO-viikko).
## Ajastamattomat sessiot jätetään pois. Mukana vain jaksot joilla on dataa.
## metric: "sessions", "duration_min" tai "distance_km" (actual-arvoista).
## activity_slug rajaa sarjan yhteen aktiviteettiin, None = kaikki.
def build_series(sessions: list[SessionInput], metric: str, period: str, activity_slug: str | None = None) -> list[dict]:
    if metric not in ["sessions", "duration_min", "distance_km"]:
        raise ValueError("Unknown metric")
    if period not in ["week", "month"]:
        raise ValueError("Unknown period")

    buckets = {}
    for session in sessions:
        if session.session_at is None:
            continue

        day = session.session_at.date()
        if period == "week":
            year, week, weekday = day.isocalendar()
            start = day - timedelta(days=weekday - 1)
            label = f"{year}-W{week:02d}"
        else:
            start = date(day.year, day.month, 1)
            label = f"{day.year}-{day.month:02d}"



        value = 0.0
        if metric == "sessions":
            if activity_slug is None:
                value = 1
            else:
                for m in session.measurements:
                    if m.activity_slug == activity_slug:
                        value = 1
        else:
            for m in session.measurements:
                if activity_slug is not None and m.activity_slug != activity_slug:
                    continue
                if m.unit_slug == metric and m.actual_value is not None:
                    value += m.actual_value

        if metric == "sessions" and value == 0:
            continue

        if label not in buckets:
            buckets[label] = {"period_label": label, "period_start": start.isoformat(), "value": 0}
        buckets[label]["value"] += value

    points = list(buckets.values())
    points.sort(key=lambda point: point["period_start"])
    return points
