"""PokéAPI HTTP client, cache, and generation catalog fetching."""

from __future__ import annotations

import asyncio
import json
from hashlib import sha256
from pathlib import Path
from typing import Any

import httpx

from scripts.import_catalog.pokemon_normalizer import normalize_pokemon

API_ROOT = "https://pokeapi.co/api/v2"
CACHE_DIR = Path(__file__).resolve().parent / ".cache" / "pokeapi-v2"


class PokeApiClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0),
            headers={"User-Agent": "pokemon-13-0-catalog-import/0.1"},
        )
        self._semaphore = asyncio.Semaphore(4)

    async def __aenter__(self) -> PokeApiClient:
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self._client.__aexit__(*exc_info)

    async def get_json(self, url: str) -> dict[str, Any]:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_key = sha256(url.encode("utf-8")).hexdigest()
        cache_path = CACHE_DIR / f"{cache_key}.json"
        if cache_path.exists():
            return json.loads(cache_path.read_text(encoding="utf-8"))

        payload: dict[str, Any] | None = None
        for attempt in range(5):
            try:
                async with self._semaphore:
                    response = await self._client.get(url)
                    response.raise_for_status()
                    payload = response.json()
                break
            except httpx.HTTPStatusError as exc:
                retryable = exc.response.status_code == 429 or exc.response.status_code >= 500
                if not retryable or attempt == 4:
                    raise
            except httpx.TransportError:
                if attempt == 4:
                    raise
            await asyncio.sleep(min(2**attempt, 8))

        if payload is None:
            raise RuntimeError(f"No response body received from PokéAPI for {url}")
        cache_path.write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        return payload


async def fetch_generation_records(max_generation: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    async with PokeApiClient() as client:
        for generation_number in range(1, max_generation + 1):
            generation = await client.get_json(
                f"{API_ROOT}/generation/{generation_number}/"
            )
            species_refs = generation["pokemon_species"]
            print(
                f"Generation {generation_number}: fetching {len(species_refs)} species",
                flush=True,
            )

            async def fetch_species(species_ref: dict[str, Any]) -> dict[str, Any]:
                species = await client.get_json(species_ref["url"])
                varieties = [
                    variety
                    for variety in species["varieties"]
                    if not any(
                        marker in variety["pokemon"]["name"]
                        for marker in ("-mega", "-primal", "-gmax", "-gigantamax", "-totem")
                    )
                ]
                if not any(variety["is_default"] for variety in varieties):
                    raise ValueError(f"No default variety for {species['name']}")

                async def fetch_variety(variety: dict[str, Any]) -> dict[str, Any]:
                    pokemon = await client.get_json(variety["pokemon"]["url"])
                    return normalize_pokemon(
                        species,
                        pokemon,
                        is_default_variety=variety["is_default"],
                    )

                return await asyncio.gather(*(fetch_variety(variety) for variety in varieties))

            generation_records = await asyncio.gather(
                *(fetch_species(species_ref) for species_ref in species_refs)
            )
            for species_records in generation_records:
                records.extend(species_records)

    by_external_key = {record["external_key"]: record for record in records}
    return sorted(
        by_external_key.values(), key=lambda record: record["national_dex_number"]
    )
