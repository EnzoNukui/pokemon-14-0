"""Errors for run-level battle ordering and progression."""


class BattleProgressionError(Exception):
    """Base exception for run battle progression errors."""


class BattleRunNotFound(BattleProgressionError):
    pass


class BattleProgressionUnavailable(BattleProgressionError):
    pass


class BattlePathConfigurationError(BattleProgressionError):
    pass


class BattleOrderConflict(BattleProgressionError):
    pass
