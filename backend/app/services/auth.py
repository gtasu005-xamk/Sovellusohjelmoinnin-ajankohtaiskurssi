from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories import user as user_repo


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
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


def authenticate_user(db: Session, *, email: str, password: str) -> str:
    user = user_repo.get_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError()

    return create_access_token(user.id)
