"""Dependencies that resolve the authenticated account from a bearer token."""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import TokenConfigurationError, decode_access_token
from app.db.models.user import User
from app.db.session import get_session

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized

    try:
        user_id = decode_access_token(credentials.credentials)
    except TokenConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured on this server.",
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise unauthorized from exc

    user = await session.scalar(select(User).where(User.id == user_id))
    # End the read transaction before application services start their own
    # explicit write transactions on the request's shared AsyncSession.
    await session.commit()
    if user is None or not user.is_active:
        raise unauthorized
    return user
