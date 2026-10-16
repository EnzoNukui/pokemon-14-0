from sqlalchemy import and_
from sqlalchemy.sql.elements import ColumnElement

from app.db.models.run import Run
from app.modules.runs.domain.ownership import RunOwner


def run_owner_condition(owner: RunOwner) -> ColumnElement[bool]:
    if owner.user_id is not None:
        return and_(Run.user_id == owner.user_id, Run.guest_session_id.is_(None))
    return and_(Run.user_id.is_(None), Run.guest_session_id == owner.guest_session_id)
