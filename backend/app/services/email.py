def send_password_reset_email(email: str, reset_link: str) -> None:
    print(f"Password reset link for {email}: {reset_link}")


def send_email_verification_email(email: str, verification_link: str) -> None:
    print(f"Email verification link for {email}: {verification_link}")
