from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.session import get_session
from app.modules.accounts.presentation.dependencies import get_optional_current_user
from app.modules.runs.application.guest_sessions import get_guest_session_id
from app.modules.runs.domain.ownership import RunOwner


async def get_optional_run_owner(
    user: User | None = Depends(get_optional_current_user),
    guest_token: str | None = Header(default=None, alias="X-Guest-Session"),
    session: AsyncSession = Depends(get_session),
) -> RunOwner | None:
    if user is not None:
        return RunOwner(user_id=user.id)
    if guest_token:
        guest_session_id = await get_guest_session_id(session, token=guest_token)
        if guest_session_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Guest session is invalid or expired.",
            )
        # The application services start their own explicit transactions.
        await session.commit()
        return RunOwner(guest_session_id=guest_session_id)
    return None


async def require_run_owner(
    owner: RunOwner | None = Depends(get_optional_run_owner),
) -> RunOwner:
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A bearer token or active guest session is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return owner
