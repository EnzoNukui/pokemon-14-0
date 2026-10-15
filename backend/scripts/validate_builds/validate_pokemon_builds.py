"""Validate all stored build candidates with Pokémon Showdown.

Run from backend/ after installing battle-engine dependencies:
    python -m scripts.validate_builds.validate_pokemon_builds --apply
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import select, update

from app.db.models.pokemon import Pokemon, PokemonBuild
from app.db.session import engine, session_factory

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SHOWDOWN_VALIDATOR = PROJECT_ROOT / "battle-engine" / "scripts" / "validate-builds.cjs"
DEFAULT_FORMAT = "gen9nationaldexag"
BUILD_KEY = "gen9-generated-v1"


async def load_candidates() -> list[tuple[Pokemon, PokemonBuild]]:
    async with session_factory() as session:
        result = await session.execute(
            select(Pokemon, PokemonBuild)
            .join(PokemonBuild, PokemonBuild.pokemon_id == Pokemon.id)
            .where(PokemonBuild.build_key == BUILD_KEY)
            .order_by(Pokemon.national_dex_number)
        )
        return list(result.all())


def validate_with_showdown(
    candidates: list[tuple[Pokemon, PokemonBuild]], format_id: str
) -> list[dict[str, Any]]:
    payload = [
        {
            "pokemon_id": str(pokemon.id),
            "name": pokemon.name,
            "form_name": pokemon.form_name,
            "build": {
                "ability": build.ability,
                "held_item": build.held_item,
                "moves": build.moves,
                "nature": build.nature,
                "evs": build.evs,
                "ivs": build.ivs,
            },
        }
        for pokemon, build in candidates
    ]
    process = subprocess.run(
        ["node", str(SHOWDOWN_VALIDATOR), format_id],
        cwd=SHOWDOWN_VALIDATOR.parent.parent,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(
            "Pokémon Showdown validation process failed:\n"
            f"{process.stderr.strip() or process.stdout.strip()}"
        )
    try:
        response = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Showdown returned invalid JSON: {process.stdout[:500]}"
        ) from exc
    if response.get("format") != format_id:
        raise RuntimeError("Showdown returned a result for an unexpected format.")
    results = response.get("results")
    if not isinstance(results, list) or len(results) != len(candidates):
        raise RuntimeError("Showdown did not return one result per candidate build.")
    return results


async def persist_results(
    candidates: list[tuple[Pokemon, PokemonBuild]],
    results: list[dict[str, Any]],
    format_id: str,
) -> None:
    results_by_id = {result["pokemon_id"]: result for result in results}
    validated_at = datetime.now(timezone.utc)
    async with session_factory.begin() as session:
        for pokemon, build in candidates:
            result = results_by_id[str(pokemon.id)]
            # The draft requires exactly one default build per species. Retire
            # previous-generation defaults before activating this Gen IX build.
            await session.execute(
                update(PokemonBuild)
                .where(
                    PokemonBuild.pokemon_id == pokemon.id,
                    PokemonBuild.id != build.id,
                    PokemonBuild.is_default.is_(True),
                )
                .values(is_default=False)
            )
            build.validation_status = "VALID" if result["valid"] else "INVALID"
            build.validated_format = format_id
            build.validation_errors = result["errors"]
            build.validated_at = validated_at
            build.is_default = bool(result["valid"] and pokemon.is_draft_eligible)
            if result.get("repaired_build"):
                build.ability = result["repaired_build"]["ability"]
                build.moves = result["repaired_build"]["moves"]
            session.add(build)


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        default=DEFAULT_FORMAT,
        help=f"Showdown format identifier (default: {DEFAULT_FORMAT}).",
    )
    parser.add_argument(
        "--pokemon-name",
        action="append",
        help="Validate only the named species; may be repeated for exceptions.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Persist validation status and activate valid builds as defaults.",
    )
    args = parser.parse_args()

    try:
        if not SHOWDOWN_VALIDATOR.is_file():
            raise RuntimeError(f"Showdown validator not found at {SHOWDOWN_VALIDATOR}")
        candidates = await load_candidates()
        if args.pokemon_name:
            requested_names = {name.casefold() for name in args.pokemon_name}
            candidates = [
                pair for pair in candidates if pair[0].name.casefold() in requested_names
            ]
        if not candidates:
            raise RuntimeError(f"No builds found for build key {BUILD_KEY!r}.")

        results = validate_with_showdown(candidates, args.format)
        valid_count = sum(bool(result["valid"]) for result in results)
        invalid_count = len(results) - valid_count
        print(
            f"Format: {args.format}\n"
            f"Candidates: {len(results)}\n"
            f"Valid: {valid_count}\n"
            f"Invalid: {invalid_count}"
        )
        for result in results:
            if not result["valid"]:
                print(f"\n{result['name']} ({result['pokemon_id']}):")
                for error in result["errors"]:
                    print(f"  - {error}")

        if args.apply:
            await persist_results(candidates, results, args.format)
            print("Validation statuses saved; valid builds marked as defaults.")
        else:
            print("Dry run only; pass --apply to save the results.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
