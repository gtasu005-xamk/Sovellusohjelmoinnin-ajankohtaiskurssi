import bcrypt

def hash_password(plain: str) -> str:
    password_bytes = plain.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain: str, password_hash: str) -> bool:
    password_bytes = plain.encode('utf-8')
    return bcrypt.checkpw(password_bytes, password_hash.encode('utf-8'))