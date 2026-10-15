"""Normalize PokéAPI resources and create deterministic Gen IX build candidates."""

from __future__ import annotations

from hashlib import sha256
from random import Random
from collections import defaultdict
from typing import Any

MAX_SUPPORTED_GENERATION = 9
BUILD_KEY = "gen9-generated-v1"
SUPPORTED_VERSION_GROUPS = (
    "scarlet-violet",
    "brilliant-diamond-shining-pearl",
    "sword-shield",
    "lets-go-pikachu-lets-go-eevee",
    "ultra-sun-ultra-moon",
    "sun-moon",
    "omega-ruby-alpha-sapphire",
    "x-y",
    "black-2-white-2",
    "black-white",
    "heartgold-soulsilver",
    "platinum",
    "diamond-pearl",
    "firered-leafgreen",
    "emerald",
    "ruby-sapphire",
    "crystal",
    "gold-silver",
    "yellow",
    "red-blue",
    "red-green",
)
PSEUDO_LEGENDARY_SPECIES = {
    "dragonite",
    "tyranitar",
    "salamence",
    "metagross",
    "garchomp",
    "hydreigon",
    "goodra",
    "kommo-o",
    "dragapult",
    "baxcalibur",
}


def normalize_pokemon(
    species: dict[str, Any], pokemon: dict[str, Any], *, is_default_variety: bool = True
) -> dict[str, Any]:
    type_slots = sorted(pokemon["types"], key=lambda item: item["slot"])
    national_dex_number = next(
        (
            entry["entry_number"]
            for entry in species["pokedex_numbers"]
            if entry["pokedex"]["name"] == "national"
        ),
        species["id"],
    )
    generation_url = species["generation"]["url"].rstrip("/")
    generation = int(generation_url.rsplit("/", 1)[-1])
    pokemon_name = pokemon["name"]
    form_name = None
    if not is_default_variety:
        prefix = f"{species['name']}-"
        form_name = pokemon_name[len(prefix):] if pokemon_name.startswith(prefix) else pokemon_name
    sprites = pokemon.get("sprites") or {}
    cries = pokemon.get("cries") or {}
    base_stats = {stat["stat"]["name"]: stat["base_stat"] for stat in pokemon["stats"]}
    build = generate_default_build(species, pokemon, base_stats)

    return {
        "external_key": f"pokeapi:pokemon/{pokemon['id']}",
        # Use the canonical species name (e.g. "Basculin" rather than the
        # default form resource name ("basculin-red-striped").
        "name": species["name"],
        "form_name": form_name,
        "national_dex_number": national_dex_number,
        "generation": generation,
        "primary_type": type_slots[0]["type"]["name"],
        "secondary_type": type_slots[1]["type"]["name"] if len(type_slots) > 1 else None,
        "base_stats": base_stats,
        "is_legendary": species["is_legendary"],
        "is_mythical": species["is_mythical"],
        "is_pseudo_legendary": species["name"] in PSEUDO_LEGENDARY_SPECIES,
        "is_draft_eligible": is_default_variety,
        "front_sprite_url": sprites.get("front_default"),
        "back_sprite_url": sprites.get("back_default"),
        "cry_url": cries.get("latest"),
        "data_source": "PokeAPI v2",
        "default_build": build,
    }


def generate_default_build(
    species: dict[str, Any], pokemon: dict[str, Any], base_stats: dict[str, int]
) -> dict[str, Any]:
    """Create a candidate build from the newest learnset available to each species."""
    moves_by_version: dict[str, set[str]] = defaultdict(set)
    for move_entry in pokemon["moves"]:
        for detail in move_entry["version_group_details"]:
            version_group = detail["version_group"]["name"]
            if version_group in SUPPORTED_VERSION_GROUPS:
                moves_by_version[version_group].add(move_entry["move"]["name"])
    legal_moves = next(
        (moves_by_version[group] for group in SUPPORTED_VERSION_GROUPS if moves_by_version[group]),
        set(),
    )
    if not legal_moves:
        raise ValueError(f"No supported-version moves found for {species['name']}")

    seed = int.from_bytes(sha256(species["name"].encode("utf-8")).digest(), "big")
    rng = Random(seed)
    moves = sorted(legal_moves)
    chosen_moves = rng.sample(moves, k=min(4, len(moves)))

    abilities = sorted(
        (
            ability["ability"]["name"]
            for ability in pokemon["abilities"]
            if not ability["is_hidden"]
        ),
        key=str,
    )
    if not abilities:
        abilities = sorted(ability["ability"]["name"] for ability in pokemon["abilities"])
    if not abilities:
        raise ValueError(f"No ability found for {species['name']}")

    is_physical = base_stats.get("attack", 0) >= base_stats.get("special-attack", 0)
    nature = "adamant" if is_physical else "modest"
    offensive_stat = "attack" if is_physical else "special-attack"
    evs = {
        stat: 0
        for stat in (
            "hp", "attack", "defense", "special-attack", "special-defense", "speed"
        )
    }
    evs[offensive_stat] = 252
    evs["speed"] = 252
    evs["hp"] = 4

    return {
        "build_key": BUILD_KEY,
        "nature": nature,
        "ability": abilities[0],
        "held_item": None,
        "moves": chosen_moves,
        "evs": evs,
        "ivs": {stat: 31 for stat in evs},
    }
