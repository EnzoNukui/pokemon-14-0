"""Use cases for account registration and password authentication."""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.db.models.user import User


class EmailAlreadyRegistered(Exception):
    """The submitted email is already associated with an account."""


class InvalidCredentials(Exception):
    """The email/password pair is invalid or the account is disabled."""


def normalize_email(email: str) -> str:
    return email.strip().lower()


async def register_account(
    session: AsyncSession, *, trainer_name: str, email: str, password: str
) -> User:
    normalized_email = normalize_email(email)
    existing_user = await session.scalar(
        select(User.id).where(User.email == normalized_email)
    )
    if existing_user is not None:
        raise EmailAlreadyRegistered

    user = User(
        trainer_name=trainer_name.strip(),
        email=normalized_email,
        password_hash=hash_password(password),
    )
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise EmailAlreadyRegistered from exc
    await session.refresh(user)
    return user


async def authenticate_account(
    session: AsyncSession, *, email: str, password: str
) -> User:
    normalized_email = normalize_email(email)
    user = await session.scalar(select(User).where(User.email == normalized_email))
    if user is None or not verify_password(password, user.password_hash):
        raise InvalidCredentials
    if not user.is_active:
        raise InvalidCredentials
    return user
