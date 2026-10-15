"""Account registration, login and authenticated profile routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import (
    TokenConfigurationError,
    create_access_token,
    ensure_auth_configured,
)
from app.db.models.user import User
from app.db.session import get_session
from app.modules.accounts.application.auth_service import (
    EmailAlreadyRegistered,
    InvalidCredentials,
    authenticate_account,
    register_account,
)
from app.modules.accounts.presentation.dependencies import get_current_user
from app.modules.accounts.presentation.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


def _token_response(user: User) -> TokenResponse:
    try:
        token = create_access_token(user.id)
    except TokenConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured on this server.",
        ) from exc
    return TokenResponse(
        access_token=token,
        expires_in=get_settings().access_token_expire_minutes * 60,
        user=UserResponse.model_validate(user),
    )


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    try:
        ensure_auth_configured()
    except TokenConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured on this server.",
        ) from exc
    try:
        user = await register_account(
            session, email=str(payload.email), password=payload.password
        )
    except EmailAlreadyRegistered as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        ) from exc
    return _token_response(user)


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    try:
        ensure_auth_configured()
    except TokenConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured on this server.",
        ) from exc
    try:
        user = await authenticate_account(
            session, email=str(payload.email), password=payload.password
        )
    except InvalidCredentials as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password is incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    return _token_response(user)


@router.get("/me", response_model=UserResponse)
async def get_my_account(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(user)
