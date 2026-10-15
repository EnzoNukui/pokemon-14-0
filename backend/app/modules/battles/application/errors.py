"""Errors from the Pokémon Showdown battle adapter and lifecycle."""


class BattleEngineUnavailable(Exception):
    """Showdown could not start or advance a battle."""


class BattleEngineResponseError(Exception):
    """Showdown returned a response that the application cannot use."""
