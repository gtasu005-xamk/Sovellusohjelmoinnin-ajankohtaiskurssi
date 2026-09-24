from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories import user as user_repo


class EmailAlreadyRegisteredError(Exception):
    pass


def register_user(db: Session, *, email: str, password: str, display_name: str) -> User:
    if user_repo.get_by_email(db, email) is not None:
        raise EmailAlreadyRegisteredError(email)

    user = user_repo.create(
        db,
        email=email,
        password_hash=hash_password(password),
        display_name=display_name,
    )
    db.commit()
    db.refresh(user)
    return user
