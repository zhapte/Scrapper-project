import hashlib
import secrets
from datetime import datetime
from datetime import timedelta

PASSWORD_RESET_EXPIRE_MINUTES = 30


def create_password_reset_token() -> str:
    return secrets.token_urlsafe(32)


def hash_password_reset_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def get_password_reset_expiration() -> datetime:
    return datetime.utcnow() + timedelta(minutes=PASSWORD_RESET_EXPIRE_MINUTES)
