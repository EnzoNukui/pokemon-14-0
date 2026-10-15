"""Map Pokémon Showdown's Gen IX singles tiers to the project's draft tiers.

Run from backend/ after applying migrations and installing battle-engine deps:
    python -m scripts.classify_catalog.classify_pokemon_tiers
    python -m scripts.classify_catalog.classify_pokemon_tiers --apply
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

from sqlalchemy import select

from app.db.models.pokemon import Pokemon
from app.db.session import engine, session_factory

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SHOWDOWN_EXPORTER = PROJECT_ROOT / "battle-engine" / "scripts" / "export-gen9-tiers.cjs"

# Ordered by current Showdown Singles viability bands. Species without a
# standard tier keep their existing project tier; newly unsupported species use
# Tier 1 pending review. Legendary/mythical offers keep their separate pool.
SHOWDOWN_TO_DRAFT_TIER = {
    "Uber": 5,
    "AG": 5,
    "OU": 5,
    "(OU)": 5,
    "UUBL": 5,
    "UU": 4,
    "RUBL": 4,
    "RU": 3,
    "NUBL": 3,
    "NU": 2,
    "PUBL": 2,
    "PU": 1,
    "ZUBL": 1,
    "ZU": 1,
    "LC": 1,
    "NFE": 1,
    "Illegal": 1,
}


async def load_catalog() -> list[Pokemon]:
    async with session_factory() as session:
        result = await session.scalars(
            select(Pokemon)
            .where(Pokemon.is_draft_eligible.is_(True))
            .order_by(Pokemon.national_dex_number, Pokemon.name)
        )
        return list(result.all())


def fetch_showdown_tiers(pokemon: list[Pokemon]) -> list[dict[str, Any]]:
    payload = [
        {"pokemon_id": str(entry.id), "name": entry.name}
        for entry in pokemon
    ]
    process = subprocess.run(
        ["node", str(SHOWDOWN_EXPORTER)],
        cwd=SHOWDOWN_EXPORTER.parent.parent,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )
    if process.returncode:
        raise RuntimeError(
            "Showdown tier export failed:\n"
            f"{process.stderr.strip() or process.stdout.strip()}"
        )
    response = json.loads(process.stdout)
    if response.get("generation") != 9 or len(response.get("results", [])) != len(pokemon):
        raise RuntimeError("Showdown did not return one Gen IX tier per catalog species.")
    return response["results"]


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Save Showdown tier labels and mapped project draft tiers to PostgreSQL.",
    )
    args = parser.parse_args()

    try:
        if not SHOWDOWN_EXPORTER.is_file():
            raise RuntimeError(f"Showdown tier exporter not found: {SHOWDOWN_EXPORTER}")
        pokemon = await load_catalog()
        if not pokemon:
            raise RuntimeError("The Pokémon catalog is empty.")
        results = fetch_showdown_tiers(pokemon)
        pokemon_by_id = {str(entry.id): entry for entry in pokemon}

        draft_counts: Counter[int] = Counter()
        competitive_counts: Counter[str] = Counter()
        unresolved: list[str] = []
        rare_count = 0
        for result in results:
            entry = pokemon_by_id[result["pokemon_id"]]
            competitive_tier = result["competitive_tier"]
            if not result["exists"] or competitive_tier not in SHOWDOWN_TO_DRAFT_TIER:
                unresolved.append(
                    f"{entry.name}: {competitive_tier or 'not found'}"
                    + (f" ({result['is_nonstandard']})" if result["is_nonstandard"] else "")
                )
                continue

            competitive_counts[competitive_tier] += 1
            if entry.is_legendary or entry.is_mythical:
                # They remain available in the independent 5% rare pool.
                rare_count += 1
                continue
            suggested_tier = SHOWDOWN_TO_DRAFT_TIER[competitive_tier]
            if competitive_tier == "Illegal" and entry.draft_tier is not None:
                suggested_tier = entry.draft_tier
            draft_counts[suggested_tier] += 1

        print(f"Catalog species: {len(pokemon)}")
        print("Gen IX Showdown Singles tiers:")
        for tier, count in sorted(competitive_counts.items()):
            print(f"  {tier}: {count}")
        print("Project tiers for non-legendary/non-mythical species:")
        for tier in range(1, 6):
            print(f"  Tier {tier}: {draft_counts[tier]}")
        print(f"Kept in separate Legendary/Mythical pool: {rare_count}")
        print(f"Needs manual review (unmapped/unavailable): {len(unresolved)}")
        for entry in unresolved:
            print(f"  - {entry}")

        if args.apply:
            async with session_factory.begin() as session:
                for result in results:
                    entry = pokemon_by_id[result["pokemon_id"]]
                    entry.competitive_tier = result["competitive_tier"]
                    mapped_tier = SHOWDOWN_TO_DRAFT_TIER.get(result["competitive_tier"])
                    if not result["exists"] or mapped_tier is None:
                        entry.draft_tier = None
                    elif entry.is_legendary or entry.is_mythical:
                        entry.draft_tier = None
                    elif result["competitive_tier"] == "Illegal" and entry.draft_tier is not None:
                        # Preserve the established project classification for
                        # legacy species without a current standard tier.
                        pass
                    else:
                        entry.draft_tier = mapped_tier
                    session.add(entry)
            print("Showdown tiers and mapped draft tiers saved.")
        else:
            print("Dry run only; pass --apply to save the classification.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
