import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  
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
    password = "Demo1234"
    client.post("/auth/register", json={"email": email, "password": password, "display_name": f"Kayttaja {name}"})
    response = client.post("/auth/login", json={"email": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def find_activity(headers, slug):
    for activity in client.get("/activity-types", headers=headers).json():
        if activity["slug"] == slug:
            return activity
    return None


def find_unit_id(activity, slug):
    for link in activity["unit_links"]:
        if link["unit_type"]["slug"] == slug:
            return link["unit_type_id"]
    return None


def create_data_for_a():
    a = login("a")
    running = find_activity(a, "running")
    duration = find_unit_id(running, "duration_min")
    distance = find_unit_id(running, "distance_km")

    session = client.post("/sessions", headers=a, json={
        "name": "A:n juoksu",
        "session_at": "2026-10-20T17:00:00Z",
        "items": [{
            "activity_type_id": running["id"],
            "measurements": [{"unit_type_id": duration, "planned_value": 30, "actual_value": 28}],
        }],
    }).json()
    plan = client.post("/plans", headers=a, json={"name": "A:n plan"}).json()
    client.post(f"/plans/{plan['id']}/sessions/{session['id']}", headers=a)
    goal = client.post("/goals", headers=a, json={"unit_type_id": distance, "target_value": 20, "period": "week"}).json()

    return a, session["id"], plan["id"], goal["id"]


def test_no_token_returns_401():
    a, session_id, plan_id, goal_id = create_data_for_a()

    assert client.get(f"/sessions/{session_id}").status_code == 401
    assert client.get(f"/plans/{plan_id}").status_code == 401
    assert client.get(f"/goals/{goal_id}").status_code == 401


def test_b_cannot_use_a_session():
    a, session_id, plan_id, goal_id = create_data_for_a()
    b = login("b")

    responses = [
        client.get(f"/sessions/{session_id}", headers=b),
        client.patch(f"/sessions/{session_id}", headers=b, json={"name": "hakkeroitu"}),
        client.delete(f"/sessions/{session_id}", headers=b),
    ]
    for response in responses:
        assert response.status_code == 404
        assert response.json()["detail"] == "Session not found"

    response = client.get(f"/sessions/{session_id}", headers=a)
    assert response.status_code == 200
    assert response.json()["name"] == "A:n juoksu"


def test_b_cannot_use_a_plan():
    a, session_id, plan_id, goal_id = create_data_for_a()
    b = login("b")

    responses = [
        client.get(f"/plans/{plan_id}", headers=b),
        client.patch(f"/plans/{plan_id}", headers=b, json={"name": "hakkeroitu"}),
        client.delete(f"/plans/{plan_id}", headers=b),
    ]
    for response in responses:
        assert response.status_code == 404
        assert response.json()["detail"] == "Plan not found"

    response = client.get(f"/plans/{plan_id}", headers=a)
    assert response.status_code == 200
    assert response.json()["name"] == "A:n plan"


def test_b_cannot_use_a_goal():
    a, session_id, plan_id, goal_id = create_data_for_a()
    b = login("b")

    responses = [
        client.get(f"/goals/{goal_id}", headers=b),
        client.patch(f"/goals/{goal_id}", headers=b, json={"active": False}),
        client.delete(f"/goals/{goal_id}", headers=b),
    ]
    for response in responses:
        assert response.status_code == 404
        assert response.json()["detail"] == "Goal not found"

    response = client.get(f"/goals/{goal_id}", headers=a)
    assert response.status_code == 200
    assert response.json()["active"] is True


def test_b_cannot_clone_or_attach_a_session():
    a, session_id, plan_id, goal_id = create_data_for_a()
    b = login("b")
    plan_b = client.post("/plans", headers=b, json={"name": "B:n plan"}).json()

    response = client.post(f"/sessions/{session_id}/clone", headers=b, json={})
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"

    response = client.post(f"/plans/{plan_b['id']}/sessions/{session_id}", headers=b)
    assert response.status_code == 404
    assert response.json()["detail"] == "Session not found"

    response = client.get(f"/sessions/{session_id}", headers=a)
    assert response.json()["plan_id"] == plan_id


def test_lists_and_calendar_only_show_own_rows():
    a, session_id, plan_id, goal_id = create_data_for_a()
    b = login("b")
    client.post("/sessions", headers=b, json={"name": "B:n sessio", "session_at": "2026-10-21T17:00:00Z"})

    session_ids = [s["id"] for s in client.get("/sessions", headers=b).json()["items"]]
    plan_ids = [p["id"] for p in client.get("/plans", headers=b).json()]
    goal_ids = [g["id"] for g in client.get("/goals", headers=b).json()]
    calendar_ids = [s["id"] for s in client.get(f"/calendar?{OCTOBER}", headers=b).json()]

    assert len(session_ids) == 1
    assert session_id not in session_ids
    assert plan_id not in plan_ids
    assert goal_id not in goal_ids
    assert session_id not in calendar_ids

    response = client.get(f"/sessions?plan_id={plan_id}", headers=b)
    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == 0

    response = client.get(f"/calendar?{OCTOBER}&plan_id={plan_id}", headers=b)
    assert response.status_code == 200
    assert response.json() == []


def test_clone_is_isolated_from_source():
    a, session_id, plan_id, goal_id = create_data_for_a()

    response = client.post(f"/sessions/{session_id}/clone", headers=a, json={"name": "Kopio"})
    assert response.status_code == 201
    clone = response.json()
    assert clone["source_session_id"] == session_id
    assert clone["plan_id"] is None
    assert clone["status"] == "planned"

    measurement = clone["items"][0]["measurements"][0]
    assert measurement["planned_value"] == 30
    assert measurement["actual_value"] is None

    running = find_activity(a, "running")
    distance = find_unit_id(running, "distance_km")
    client.patch(f"/sessions/{session_id}", headers=a, json={
        "name": "Muokattu",
        "items": [
            {"activity_type_id": running["id"], "measurements": [{"unit_type_id": distance, "planned_value": 10}]},
            {"activity_type_id": running["id"], "measurements": []},
        ],
    })

    after = client.get(f"/sessions/{clone['id']}", headers=a).json()
    assert after["name"] == "Kopio"
    assert after["items"] == clone["items"]
