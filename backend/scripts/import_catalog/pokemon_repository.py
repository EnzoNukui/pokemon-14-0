"""Persist imported Pokémon and candidate builds to PostgreSQL."""

from __future__ import annotations

from typing import Any

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func

from app.db.models.pokemon import Pokemon, PokemonBuild


async def import_records(records: list[dict[str, Any]]) -> None:
    from app.db.session import engine

    pokemon_records = [
        {key: value for key, value in record.items() if key != "default_build"}
        for record in records
    ]
    pokemon_upsert = insert(Pokemon).values(pokemon_records)
    pokemon_upsert = pokemon_upsert.on_conflict_do_update(
        index_elements=[Pokemon.external_key],
        set_={
            "name": pokemon_upsert.excluded.name,
            "form_name": pokemon_upsert.excluded.form_name,
            "national_dex_number": pokemon_upsert.excluded.national_dex_number,
            "generation": pokemon_upsert.excluded.generation,
            "primary_type": pokemon_upsert.excluded.primary_type,
            "secondary_type": pokemon_upsert.excluded.secondary_type,
            "base_stats": pokemon_upsert.excluded.base_stats,
            "is_legendary": pokemon_upsert.excluded.is_legendary,
            "is_mythical": pokemon_upsert.excluded.is_mythical,
            "is_pseudo_legendary": pokemon_upsert.excluded.is_pseudo_legendary,
            "is_draft_eligible": pokemon_upsert.excluded.is_draft_eligible,
            "front_sprite_url": pokemon_upsert.excluded.front_sprite_url,
            "back_sprite_url": pokemon_upsert.excluded.back_sprite_url,
            "cry_url": pokemon_upsert.excluded.cry_url,
            "data_source": pokemon_upsert.excluded.data_source,
            "updated_at": func.now(),
        },
    )
    async with engine.begin() as connection:
        result = await connection.execute(
            pokemon_upsert.returning(Pokemon.id, Pokemon.external_key)
        )
        ids_by_external_key = {
            external_key: pokemon_id
            for pokemon_id, external_key in result.all()
        }
        pokemon_ids = list(ids_by_external_key.values())
        await connection.execute(
            update(PokemonBuild)
            .where(PokemonBuild.pokemon_id.in_(pokemon_ids))
            .values(is_default=False)
        )

        build_records = []
        for record in records:
            build = record["default_build"]
            build_records.append(
                {
                    "pokemon_id": ids_by_external_key[record["external_key"]],
                    **build,
                    # Builds remain candidates until the selected Showdown format validates them.
                    "is_default": False,
                }
            )

        build_upsert = insert(PokemonBuild).values(build_records)
        build_upsert = build_upsert.on_conflict_do_update(
            index_elements=[PokemonBuild.pokemon_id, PokemonBuild.build_key],
            set_={
                "nature": build_upsert.excluded.nature,
                "ability": build_upsert.excluded.ability,
                "held_item": build_upsert.excluded.held_item,
                "moves": build_upsert.excluded.moves,
                "evs": build_upsert.excluded.evs,
                "ivs": build_upsert.excluded.ivs,
                "is_default": False,
                "validation_status": "PENDING",
                "validated_format": None,
                "validation_errors": [],
                "validated_at": None,
                "updated_at": func.now(),
            },
        )
        await connection.execute(build_upsert)
    await engine.dispose()
