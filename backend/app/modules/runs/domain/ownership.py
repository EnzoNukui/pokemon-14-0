from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True, slots=True)
class RunOwner:
    """Authenticated account or anonymous browser session that owns a run."""

    user_id: UUID | None = None
    guest_session_id: UUID | None = None

    def __post_init__(self) -> None:
        if (self.user_id is None) == (self.guest_session_id is None):
            raise ValueError("A run owner must be either an account or a guest session.")
