import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

def hash_password(plain: str) -> str:
    password_bytes = plain.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain: str, password_hash: str) -> bool:
    password_bytes = plain.encode('utf-8')
    return bcrypt.checkpw(password_bytes, password_hash.encode('utf-8'))

ALGORITHM = "HS256"

def  create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM], options={"require": ["exp", "sub"]})