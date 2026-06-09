import os
from datetime import datetime
from uuid import UUID

import jwt
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Security
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.auth.email_verification import create_email_verification_token
from app.auth.email_verification import get_email_verification_expiration
from app.auth.email_verification import hash_email_verification_token
from app.auth.password_reset import create_password_reset_token
from app.auth.password_reset import get_password_reset_expiration
from app.auth.password_reset import hash_password_reset_token
from app.auth.security import hash_password
from app.auth.security import verify_password
from app.auth.tokens import create_access_token
from app.auth.tokens import decode_access_token
from app.dependencies import get_db
from app.models import EmailVerificationToken
from app.models import PasswordResetToken
from app.models import User
from app.schemas import EmailVerificationRequest
from app.schemas import ForgotPasswordRequest
from app.schemas import ForgotPasswordResponse
from app.schemas import RegisterResponse
from app.schemas import ResendEmailVerificationRequest
from app.schemas import ResetPasswordRequest
from app.schemas import TokenResponse
from app.schemas import UserCreate
from app.schemas import UserLogin
from app.schemas import UserResponse
from app.services.email import send_email_verification_email
from app.services.email import send_password_reset_email

router = APIRouter(prefix="/auth", tags=["auth"])
bearer_scheme = HTTPBearer()


def create_and_send_email_verification(user: User, db: Session) -> None:
    (
        db.query(EmailVerificationToken)
        .filter(EmailVerificationToken.user_id == user.user_id)
        .filter(EmailVerificationToken.used_at.is_(None))
        .update({"used_at": datetime.utcnow()})
    )

    verification_token = create_email_verification_token()
    verification_token_hash = hash_email_verification_token(verification_token)
    email_verification_token = EmailVerificationToken(
        user_id=user.user_id,
        token_hash=verification_token_hash,
        expires_at=get_email_verification_expiration(),
    )

    db.add(email_verification_token)
    db.commit()

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    verification_link = f"{frontend_url}/?verify_email_token={verification_token}"
    send_email_verification_email(user.email, verification_link)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")
    except jwt.PyJWTError as exc:
        raise credentials_error from exc

    if not user_id:
        raise credentials_error

    user = db.query(User).filter(User.user_id == UUID(user_id)).first()

    if not user:
        raise credentials_error

    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before continuing",
        )

    return user


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    create_and_send_email_verification(user, db)

    return {
        "message": "Registration successful. Please verify your email before logging in.",
        "user": user,
    }


@router.post("/login", response_model=TokenResponse)
def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == user_data.email).first()

    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in",
        )

    access_token = create_access_token(str(user.user_id))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }


@router.post("/verify-email")
def verify_email(
    email_verification_request: EmailVerificationRequest,
    db: Session = Depends(get_db),
):
    verification_token_hash = hash_email_verification_token(
        email_verification_request.token
    )
    email_verification_token = (
        db.query(EmailVerificationToken)
        .filter(EmailVerificationToken.token_hash == verification_token_hash)
        .with_for_update()
        .first()
    )

    if (
        not email_verification_token
        or email_verification_token.used_at is not None
        or email_verification_token.expires_at < datetime.utcnow()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired email verification token",
        )

    user = (
        db.query(User)
        .filter(User.user_id == email_verification_token.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired email verification token",
        )

    user.is_email_verified = True
    email_verification_token.used_at = datetime.utcnow()
    db.commit()

    return {"message": "Email has been verified successfully. You can now log in."}


@router.post("/resend-verification")
def resend_verification(
    resend_request: ResendEmailVerificationRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == resend_request.email).first()
    response = {
        "message": "If an unverified account exists for that email, a verification link has been sent.",
    }

    if not user or user.is_email_verified:
        return response

    create_and_send_email_verification(user, db)

    return response


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(
    password_reset_request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == password_reset_request.email)
        .first()
    )
    response = {
        "message": "If an account exists for that email, a reset link has been sent.",
    }

    if not user:
        return response

    (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.user_id == user.user_id)
        .filter(PasswordResetToken.used_at.is_(None))
        .update({"used_at": datetime.utcnow()})
    )

    reset_token = create_password_reset_token()
    reset_token_hash = hash_password_reset_token(reset_token)
    password_reset_token = PasswordResetToken(
        user_id=user.user_id,
        token_hash=reset_token_hash,
        expires_at=get_password_reset_expiration(),
    )

    db.add(password_reset_token)
    db.commit()

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    reset_link = f"{frontend_url}/?reset_token={reset_token}"
    send_password_reset_email(user.email, reset_link)

    return response


@router.post("/reset-password")
def reset_password(
    password_reset_request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    reset_token_hash = hash_password_reset_token(password_reset_request.token)
    password_reset_token = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.token_hash == reset_token_hash)
        .with_for_update()
        .first()
    )

    if (
        not password_reset_token
        or password_reset_token.used_at is not None
        or password_reset_token.expires_at < datetime.utcnow()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token",
        )

    user = (
        db.query(User)
        .filter(User.user_id == password_reset_token.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token",
        )

    user.password = hash_password(password_reset_request.password)
    password_reset_token.used_at = datetime.utcnow()
    db.commit()

    return {"message": "Password has been reset successfully."}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Security(get_current_user)):
    return current_user
