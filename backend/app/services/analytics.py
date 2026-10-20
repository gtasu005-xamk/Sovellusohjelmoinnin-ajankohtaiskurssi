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
