from datetime import datetime, timedelta, timezone
from hashlib import sha256
from secrets import token_urlsafe
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.guest_session import GuestSession

GUEST_SESSION_LIFETIME = timedelta(days=30)


def hash_guest_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


async def create_guest_session(session: AsyncSession) -> tuple[GuestSession, str]:
    token = token_urlsafe(32)
    guest_session = GuestSession(
        token_hash=hash_guest_token(token),
        expires_at=datetime.now(timezone.utc) + GUEST_SESSION_LIFETIME,
    )
    session.add(guest_session)
    await session.flush()
    return guest_session, token


async def find_active_guest_session(
    session: AsyncSession, *, token: str
) -> GuestSession | None:
    now = datetime.now(timezone.utc)
    return await session.scalar(
        select(GuestSession).where(
            GuestSession.token_hash == hash_guest_token(token),
            GuestSession.expires_at > now,
        )
    )


async def get_guest_session_id(
    session: AsyncSession, *, token: str
) -> UUID | None:
    guest_session = await find_active_guest_session(session, token=token)
    return guest_session.id if guest_session is not None else None
