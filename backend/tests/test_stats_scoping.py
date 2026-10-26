import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.services.seed import seed_catalog

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)

seed_db = TestingSessionLocal()
seed_catalog(seed_db)
seed_db.commit()
seed_db.close()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def use_test_db():
    app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)

OCTOBER = "from=2026-10-01T00:00:00Z&to=2026-10-31T23:59:59Z"


def login(name):
    email = f"{name}-{uuid.uuid4().hex[:8]}@example.com"
    client.post("/auth/register", json={"email": email, "password": "Demo1234", "display_name": f"Kayttaja {name}"})
    response = client.post("/auth/login", json={"email": email, "password": "Demo1234"})
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def running_session(headers, session_at, duration, distance, intensity):
    running = None
    for activity in client.get("/activity-types", headers=headers).json():
        if activity["slug"] == "running":
            running = activity

    measurements = []
    for link in running["unit_links"]:
        if link["unit_type"]["slug"] == "duration_min":
            measurements.append({"unit_type_id": link["unit_type_id"], "actual_value": duration})
        if link["unit_type"]["slug"] == "distance_km":
            measurements.append({"unit_type_id": link["unit_type_id"], "actual_value": distance})

    client.post("/sessions", headers=headers, json={
        "name": "Juoksu",
        "session_at": session_at,
        "intensity": intensity,
        "items": [{"activity_type_id": running["id"], "measurements": measurements}],
    })


def create_two_users():
    a = login("a")
    b = login("b")
    running_session(a, "2026-10-05T17:00:00Z", 30, 5, 6)
    running_session(a, "2026-10-12T17:00:00Z", 40, 7.5, 8)
    running_session(b, "2026-10-06T17:00:00Z", 100, 50, 1)
    running_session(b, "2026-10-13T17:00:00Z", 100, 50, 1)
    running_session(b, "2026-10-20T17:00:00Z", 100, 50, 1)
    return a, b


def test_summary_only_counts_own_sessions():
    a, b = create_two_users()

    summary_a = client.get(f"/stats/summary?{OCTOBER}", headers=a).json()
    assert summary_a["session_count"] == 2
    assert summary_a["total_duration_min"] == 70
    assert summary_a["total_distance_km"] == 12.5
    assert summary_a["avg_intensity"] == 7.0

    summary_b = client.get(f"/stats/summary?{OCTOBER}", headers=b).json()
    assert summary_b["session_count"] == 3
    assert summary_b["total_distance_km"] == 150


def test_progress_only_counts_own_sessions():
    a, b = create_two_users()

    points = client.get(f"/stats/progress?{OCTOBER}&metric=distance_km&granularity=week", headers=a).json()
    values = [point["value"] for point in points]
    assert values == [5, 7.5]


def test_streaks_only_use_own_sessions():
    a = login("a")
    b = login("b")
    today = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
    for days_ago in [0, 1, 2, 3]:
        running_session(b, (today - timedelta(days=days_ago)).isoformat(), 30, 5, 5)
    running_session(a, today.isoformat(), 30, 5, 5)

    streaks_a = client.get("/stats/streaks", headers=a).json()
    assert streaks_a["current_days"] == 1
    assert streaks_a["longest_days"] == 1

    streaks_b = client.get("/stats/streaks", headers=b).json()
    assert streaks_b["current_days"] == 4


def test_user_id_from_query_is_ignored():
    a, b = create_two_users()

    normal = client.get(f"/stats/summary?{OCTOBER}", headers=a).json()
    with_user_id = client.get(f"/stats/summary?{OCTOBER}&user_id=999", headers=a).json()
    assert with_user_id == normal


def test_stats_require_login():
    assert client.get(f"/stats/summary?{OCTOBER}").status_code == 401
    assert client.get(f"/stats/progress?{OCTOBER}").status_code == 401
    assert client.get("/stats/streaks").status_code == 401
