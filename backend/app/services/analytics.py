## Analytiikka: pelkkiä laskufunktioita, ei I/O:ta.
## Ei hae tietokannasta eikä importtaa FastAPI:a tai SQLAlchemya, jotta testit toimii ilman kantaa.
## Kutsuja lataa yhden käyttäjän sessiot, rajaa ne valmiiksi
## kirjautuneeseen käyttäjään ja antaa ne tänne SessionInput-listana.
##
## SessionInput = yksi sessio (aika, status, intensiteetti ja mittaukset)
## MeasurementInput = yksi mittaus, aktiviteetti ja yksikkö sluggina (esim. running, distance_km)
## planned/actual voi olla None jos arvoa ei ole syötetty

from dataclasses import dataclass, field
from datetime import datetime

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
