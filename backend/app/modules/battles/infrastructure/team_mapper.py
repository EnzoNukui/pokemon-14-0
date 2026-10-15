"""Translate saved Pokémon builds to the Showdown engine set format."""


def to_engine_set(
    name: str, form_name: str | None, build: dict[str, object]
) -> dict[str, object]:
    return {
        "species": f"{name}-{form_name}" if form_name else name,
        "item": build.get("held_item") or "",
        "ability": build.get("ability", ""),
        "moves": build.get("moves", []),
        "nature": build.get("nature", "Serious"),
        "evs": normalize_engine_stats(build.get("evs", {})),
        "ivs": normalize_engine_stats(build.get("ivs", {})),
        "level": 100,
    }


def normalize_engine_stats(stats: object) -> dict[str, int]:
    if not isinstance(stats, dict):
        return {}
    aliases = {
        "hp": "hp",
        "attack": "atk",
        "defense": "def",
        "special-attack": "spa",
        "special-defense": "spd",
        "speed": "spe",
        "atk": "atk",
        "def": "def",
        "spa": "spa",
        "spd": "spd",
        "spe": "spe",
    }
    return {
        aliases[key]: int(value)
        for key, value in stats.items()
        if key in aliases and isinstance(value, (int, float))
    }
