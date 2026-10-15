"""Import Pokémon species I–IX and candidate Gen IX builds into PostgreSQL.

Run from backend/ with:
    python -m scripts.import_catalog.import_pokemon --apply

Without --apply, the script downloads/caches the source data and prints a summary.
Draft tiers remain unset until the separate Showdown classification step.
"""

from __future__ import annotations

import argparse
import asyncio

from scripts.import_catalog.pokeapi_client import fetch_generation_records
from scripts.import_catalog.pokemon_normalizer import MAX_SUPPORTED_GENERATION
from scripts.import_catalog.pokemon_repository import import_records


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-generation",
        type=int,
        default=MAX_SUPPORTED_GENERATION,
        choices=range(1, MAX_SUPPORTED_GENERATION + 1),
        help="Import species up to this generation (default: 9).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Upsert the fetched catalog into PostgreSQL; without this, only fetch and summarize.",
    )
    args = parser.parse_args()

    records = await fetch_generation_records(args.max_generation)
    print(
        f"Prepared {len(records)} Pokémon catalog entries through generation "
        f"{args.max_generation}."
    )
    if args.apply:
        await import_records(records)
        print("Pokémon catalog upsert completed.")
    else:
        print("Dry run only; pass --apply to write the catalog to PostgreSQL.")


if __name__ == "__main__":
    asyncio.run(main())
