"""Import the curated trainer roster and its validated Gen IX teams.

Run from backend/:
    python -m scripts.import_trainers.import_trainer_roster
    python -m scripts.import_trainers.import_trainer_roster --apply
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path
from typing import Any

from sqlalchemy import delete, func, select

from app.db.models import Pokemon, PokemonBuild, Trainer, TrainerTeam, TrainerTeamPokemon
from app.db.session import engine, session_factory

PROJECT_ROOT = Path(__file__).resolve().parents[3]
ROSTER_PATH = PROJECT_ROOT / "database" / "seeds" / "trainers" / "elenco_aprovado.json"
BUILD_KEY = "gen9-generated-v1"
FORMAT_ID = "gen9nationaldexag"


def normalize_pokemon_name(value: str) -> str:
    """Match human-readable team names to the normalized catalogue name."""
    value_without_notes = re.sub(r"\s*\([^)]*\)", "", value.strip())
    normalized = re.sub(r"[^a-z0-9]", "", value_without_notes.casefold())
    # Preserve the original source's misspelling as an explicit data alias.
    return {"camelrupt": "camerupt"}.get(normalized, normalized)


def load_roster() -> dict[str, Any]:
    with ROSTER_PATH.open(encoding="utf-8") as roster_file:
        return json.load(roster_file)


async def prepare(session, roster: dict[str, Any]) -> list[dict[str, Any]]:
    rows = await session.execute(
        select(Pokemon, PokemonBuild)
        .join(PokemonBuild, PokemonBuild.pokemon_id == Pokemon.id)
        .where(
            PokemonBuild.build_key == BUILD_KEY,
            PokemonBuild.validation_status == "VALID",
            PokemonBuild.validated_format == FORMAT_ID,
        )
    )
    builds: dict[tuple[str, str | None], tuple[Pokemon, PokemonBuild]] = {}
    for pokemon, build in rows.all():
        key = (normalize_pokemon_name(pokemon.name), pokemon.form_name)
        builds[key] = (pokemon, build)

    prepared: list[dict[str, Any]] = []
    problems: list[str] = []
    for trainer_data in roster["trainers"]:
        team_data_rows = []
        for team_data in trainer_data["teams"]:
            members = []
            for slot_number, member_data in enumerate(team_data["members"], start=1):
                if isinstance(member_data, str):
                    member_name, form_name = member_data, None
                else:
                    member_name = member_data["name"]
                    form_name = member_data.get("form")
                pokemon_key = (normalize_pokemon_name(member_name), form_name)
                found = builds.get(pokemon_key)
                if found is None:
                    problems.append(
                        f"{trainer_data['name']} / {team_data['team_key']} / "
                        f"slot {slot_number}: missing valid Gen IX build for "
                        f"{member_name} (form={form_name!r})"
                    )
                    continue
                pokemon, build = found
                members.append((slot_number, pokemon, build))
            if team_data["active"] and len(team_data["members"]) != 6:
                problems.append(
                    f"{trainer_data['name']} / {team_data['team_key']}: active team "
                    f"has {len(team_data['members'])} members, expected 6"
                )
            if team_data["active"] and len(members) != 6:
                problems.append(
                    f"{trainer_data['name']} / {team_data['team_key']}: active team "
                    "does not resolve to six valid builds"
                )
            team_data_rows.append((team_data, members))
        prepared.append((trainer_data, team_data_rows))
    if problems:
        raise ValueError("Roster validation failed:\n- " + "\n- ".join(problems))
    return prepared


async def import_roster(*, apply: bool) -> None:
    roster = load_roster()
    async with session_factory() as session:
        prepared = await prepare(session, roster)
        trainers_count = len(prepared)
        teams_count = sum(len(teams) for _, teams in prepared)
        active_count = sum(
            bool(team_data["active"])
            for _, teams in prepared
            for team_data, _ in teams
        )
        member_count = sum(
            len(members)
            for _, teams in prepared
            for _, members in teams
        )
        if not apply:
            print(
                f"Validated {trainers_count} trainers, {teams_count} teams "
                f"({active_count} active), and {member_count} Pokémon entries. "
                "No database changes made; pass --apply to import."
            )
            return

        # `prepare` queried the catalogue and opened an implicit read transaction.
        # End it before opening the write transaction; expire_on_commit=False keeps
        # the resolved ORM rows usable while applying the prepared seed.
        await session.commit()
        async with session.begin():
            for trainer_data, teams in prepared:
                matching_trainers = list(
                    (
                        await session.scalars(
                            select(Trainer).where(
                                func.lower(Trainer.name)
                                == trainer_data["name"].casefold()
                            )
                        )
                    ).all()
                )
                if len(matching_trainers) > 1:
                    raise ValueError(
                        f"Multiple database trainers match {trainer_data['name']!r}."
                    )
                trainer = matching_trainers[0] if matching_trainers else Trainer(
                    name=trainer_data["name"]
                )
                trainer.name = trainer_data["name"]
                trainer.region = trainer_data.get("region")
                trainer.sprite_url = trainer_data.get("sprite_url")
                trainer.sprite_source = trainer_data.get("sprite_source")
                trainer.sprite_credit = trainer_data.get("sprite_credit")
                trainer.notes = trainer_data.get("notes")
                session.add(trainer)
                await session.flush()

                for team_data, members in teams:
                    matching_teams = list(
                        (
                            await session.scalars(
                                select(TrainerTeam).where(
                                    TrainerTeam.trainer_id == trainer.id,
                                    TrainerTeam.team_key == team_data["team_key"],
                                )
                            )
                        ).all()
                    )
                    team = matching_teams[0] if matching_teams else TrainerTeam(
                        trainer_id=trainer.id,
                        team_key=team_data["team_key"],
                        anime_period=team_data["anime_period"],
                        category=team_data["category"],
                    )
                    team.category = team_data["category"]
                    team.difficulty_tier = team_data.get("difficulty_tier")
                    team.anime_period = team_data["anime_period"]
                    team.source_url = team_data.get("source_url")
                    team.source_notes = team_data.get("source_notes")
                    team.is_active = team_data["active"]
                    session.add(team)
                    await session.flush()

                    await session.execute(
                        delete(TrainerTeamPokemon).where(
                            TrainerTeamPokemon.trainer_team_id == team.id
                        )
                    )
                    for slot_number, pokemon, build in members:
                        session.add(
                            TrainerTeamPokemon(
                                trainer_team_id=team.id,
                                pokemon_id=pokemon.id,
                                slot_number=slot_number,
                                nature=build.nature,
                                ability=build.ability,
                                held_item=build.held_item,
                                moves=build.moves,
                                evs=build.evs,
                                ivs=build.ivs,
                            )
                        )
            await session.flush()
        print(
            f"Imported {trainers_count} trainers, {teams_count} teams "
            f"({active_count} active), and {member_count} Pokémon entries."
        )


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write the validated roster into PostgreSQL; omit for dry-run.",
    )
    args = parser.parse_args()
    try:
        await import_roster(apply=args.apply)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
