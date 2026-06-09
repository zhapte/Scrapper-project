import hashlib
import secrets
from datetime import datetime
from datetime import timedelta

EMAIL_VERIFICATION_EXPIRE_HOURS = 24


def create_email_verification_token() -> str:
    return secrets.token_urlsafe(32)


def hash_email_verification_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def get_email_verification_expiration() -> datetime:
    return datetime.utcnow() + timedelta(hours=EMAIL_VERIFICATION_EXPIRE_HOURS)
