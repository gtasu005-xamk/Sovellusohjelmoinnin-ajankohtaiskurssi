from app.db.session import SessionLocal
from app.services.seed import seed_catalog


def init_db() -> None:
    db = SessionLocal()
    try:
        seed_catalog(db)
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
