"""HTTP client for the local Pokémon Showdown simulation service."""

from __future__ import annotations

from typing import Any
from uuid import UUID

import httpx

from app.core.config import get_settings


class ShowdownUnavailable(Exception):
    """Showdown could not start or advance a battle."""


class ShowdownClient:
    def __init__(self) -> None:
        settings = get_settings()
        self._base_url = settings.battle_engine_url.rstrip("/")
        self._timeout = settings.battle_engine_timeout_seconds

    async def start_battle(
        self,
        *,
        battle_id: UUID,
        player_name: str,
        player_team: list[dict[str, Any]],
        opponent_name: str,
        opponent_team: list[dict[str, Any]],
        battle_format: str,
    ) -> dict[str, Any]:
        return await self._request(
            "POST",
            "/battles",
            json={
                "battle_id": str(battle_id),
                "format": battle_format,
                "player": {"name": player_name, "team": player_team},
                "opponent": {"name": opponent_name, "team": opponent_team},
            },
        )

    async def submit_choice(self, *, battle_id: UUID, choice: str) -> dict[str, Any]:
        return await self._request(
            "POST", f"/battles/{battle_id}/choices", json={"choice": choice}
        )

    async def get_battle(self, *, battle_id: UUID) -> dict[str, Any]:
        return await self._request("GET", f"/battles/{battle_id}")

    async def abandon_battle(self, *, battle_id: UUID) -> None:
        await self._request("DELETE", f"/battles/{battle_id}")

    async def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(
                base_url=self._base_url, timeout=self._timeout
            ) as client:
                response = await client.request(method, path, **kwargs)
                if response.status_code == 204:
                    return {"status": "ABANDONED"}
                response.raise_for_status()
                payload = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            detail = "Showdown engine did not return a valid response."
            if isinstance(exc, httpx.HTTPStatusError):
                try:
                    detail = str(exc.response.json().get("detail", detail))
                except ValueError:
                    pass
            elif isinstance(exc, httpx.RequestError):
                detail = "Showdown engine is unavailable. Start the battle-engine service."
            raise ShowdownUnavailable(detail) from exc

        if not isinstance(payload, dict):
            raise ShowdownUnavailable("Showdown engine returned an invalid response.")
        return payload
