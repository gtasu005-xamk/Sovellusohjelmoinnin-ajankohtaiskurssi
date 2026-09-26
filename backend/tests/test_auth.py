import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app import models  # noqa: F401  rekisteröi taulut Base.metadataan
from app.db.base import Base
from app.db.session import get_db
from app.main import app

# SQLite-muistikanta testejä varten, StaticPool pitää saman yhteyden koko ajon ajan
engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_me_without_token_returns_401():
    assert client.get("/auth/me").status_code == 401


def test_register_login_me():
    email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    password = "Demo1234"

    response = client.post(
        "/auth/register",
        json={"email": email, "password": password, "display_name": "Test User"},
    )
    assert response.status_code == 201

    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == email
