import os
from datetime import datetime
from datetime import timedelta
from datetime import timezone

import jwt

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def get_secret_key() -> str:
    secret_key = os.getenv("SECRET_KEY")

    if secret_key:
        return secret_key

    return "change-this-secret-key"


def create_access_token(subject: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": subject,
        "exp": expires_at,
    }

    return jwt.encode(payload, get_secret_key(), algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, get_secret_key(), algorithms=[JWT_ALGORITHM])
