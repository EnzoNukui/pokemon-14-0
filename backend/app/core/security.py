"""Password hashing and signed access-token helpers."""

from datetime import datetime, timedelta, timezone
from functools import lru_cache
from typing import Any
from uuid import UUID

import jwt
from pwdlib import PasswordHash

from app.core.config import Settings, get_settings

JWT_ALGORITHM = "HS256"


@lru_cache
def get_password_hasher() -> PasswordHash:
    return PasswordHash.recommended()


def hash_password(password: str) -> str:
    return get_password_hasher().hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return get_password_hasher().verify(password, password_hash)


class TokenConfigurationError(RuntimeError):
    """Raised when the server has no safe signing key configured."""


def _signing_key(settings: Settings) -> str:
    secret = settings.auth_secret_key
    if secret is None:
        raise TokenConfigurationError("AUTH_SECRET_KEY must be configured.")
    value = secret.get_secret_value()
    if len(value.encode("utf-8")) < 32:
        raise TokenConfigurationError(
            "AUTH_SECRET_KEY must contain at least 32 bytes."
        )
    return value


def ensure_auth_configured() -> None:
    """Fail early before performing account changes if signing is unavailable."""
    _signing_key(get_settings())


def create_access_token(subject: UUID) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": now,
        "exp": expires_at,
    }
    return jwt.encode(payload, _signing_key(settings), algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> UUID:
    settings = get_settings()
    payload = jwt.decode(
        token,
        _signing_key(settings),
        algorithms=[JWT_ALGORITHM],
        options={"require": ["sub", "iat", "exp"]},
    )
    subject = payload.get("sub")
    if not isinstance(subject, str):
        raise jwt.InvalidTokenError("Token subject is invalid.")
    try:
        return UUID(subject)
    except ValueError as exc:
        raise jwt.InvalidTokenError("Token subject is invalid.") from exc
