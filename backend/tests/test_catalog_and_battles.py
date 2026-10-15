import unittest

from app.modules.battles.domain.outcomes import SimulatorResult, resolve_run_battle_result
from app.modules.battles.infrastructure.team_mapper import normalize_engine_stats, to_engine_set
from scripts.import_catalog.pokemon_normalizer import normalize_pokemon


def sample_pokeapi_resources() -> tuple[dict, dict]:
    species = {
        "id": 25,
        "name": "pikachu",
        "generation": {"url": "https://pokeapi.co/api/v2/generation/1/"},
        "pokedex_numbers": [
            {"entry_number": 25, "pokedex": {"name": "national"}}
        ],
        "is_legendary": False,
        "is_mythical": False,
    }
    pokemon = {
        "id": 25,
        "name": "pikachu",
        "types": [{"slot": 1, "type": {"name": "electric"}}],
        "sprites": {"front_default": "front.png", "back_default": "back.png"},
        "cries": {"latest": "cry.ogg"},
        "stats": [
            {"stat": {"name": "attack"}, "base_stat": 55},
            {"stat": {"name": "special-attack"}, "base_stat": 50},
        ],
        "abilities": [
            {"ability": {"name": "static"}, "is_hidden": False},
            {"ability": {"name": "lightning-rod"}, "is_hidden": True},
        ],
        "moves": [
            {
                "move": {"name": move},
                "version_group_details": [
                    {"version_group": {"name": "sun-moon"}}
                ],
            }
            for move in ("thunderbolt", "quick-attack", "iron-tail", "protect", "volt-tackle")
        ],
    }
    return species, pokemon


class CatalogNormalizationTests(unittest.TestCase):
    def test_normalization_is_deterministic_and_builds_up_to_four_moves(self) -> None:
        species, pokemon = sample_pokeapi_resources()

        first = normalize_pokemon(species, pokemon)
        second = normalize_pokemon(species, pokemon)

        self.assertEqual(first, second)
        self.assertEqual(first["name"], "pikachu")
        self.assertEqual(first["national_dex_number"], 25)
        self.assertEqual(first["primary_type"], "electric")
        self.assertEqual(first["default_build"]["ability"], "static")
        self.assertEqual(len(first["default_build"]["moves"]), 4)
        self.assertEqual(len(set(first["default_build"]["moves"])), 4)

    def test_normalization_rejects_species_without_supported_moves(self) -> None:
        species, pokemon = sample_pokeapi_resources()
        pokemon["moves"] = []

        with self.assertRaisesRegex(ValueError, "No supported-version moves"):
            normalize_pokemon(species, pokemon)


class BattleMappingTests(unittest.TestCase):
    def test_saved_build_stats_are_mapped_to_showdown_keys(self) -> None:
        stats = normalize_engine_stats(
            {
                "hp": 4,
                "attack": 252,
                "defense": 0,
                "special-attack": 0,
                "special-defense": 0,
                "speed": 252,
            }
        )
        self.assertEqual(
            stats,
            {"hp": 4, "atk": 252, "def": 0, "spa": 0, "spd": 0, "spe": 252},
        )

        engine_set = to_engine_set(
            "Pikachu",
            None,
            {
                "nature": "Jolly",
                "ability": "Static",
                "held_item": None,
                "moves": ["Thunderbolt", "Quick Attack"],
                "evs": {"attack": 252, "speed": 252},
                "ivs": {"attack": 31, "speed": 31},
            },
        )
        self.assertEqual(engine_set["species"], "Pikachu")
        self.assertEqual(engine_set["evs"], {"atk": 252, "spe": 252})
        self.assertEqual(engine_set["moves"], ["Thunderbolt", "Quick Attack"])

    def test_simulator_draw_is_converted_to_a_run_loss(self) -> None:
        self.assertEqual(resolve_run_battle_result(SimulatorResult.DRAW).value, "LOSS")


if __name__ == "__main__":
    unittest.main()
