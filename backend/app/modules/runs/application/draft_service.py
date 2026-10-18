from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal
from hashlib import sha256
from random import Random
from secrets import randbits
from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.pokemon import Pokemon, PokemonBuild
from app.db.models.run import Run, RunDraftOption
from app.db.models.team import Team, TeamPokemon
from app.modules.runs.domain.draft_policy import DraftProbabilityPolicy
from app.modules.runs.domain.rules import (
    DRAFT_OPTIONS_PER_ROUND,
    DRAFT_ROUNDS,
    LEGENDARY_OFFER_PROBABILITY,
    REROLLS_PER_RUN,
)
from app.modules.runs.domain.states import RunStage, RunStatus
from app.modules.runs.application.ownership import run_owner_condition
from app.modules.runs.domain.ownership import RunOwner


class DraftError(Exception):
    """Base class for expected draft rule or catalog errors."""


class RunNotFound(DraftError):
    pass


class DraftUnavailable(DraftError):
    pass


class DraftCompleted(DraftError):
    pass


class InvalidDraftSelection(DraftError):
    pass


class RerollUnavailable(DraftError):
    pass


class DraftPoolConfigurationError(DraftError):
    pass


@dataclass(frozen=True, slots=True)
class DraftOptionView:
    option_number: int
    pokemon_id: UUID
    name: str
    form_name: str | None
    primary_type: str
    secondary_type: str | None
    draft_tier: int | None
    is_legendary: bool
    is_mythical: bool
    is_pseudo_legendary: bool
    front_sprite_url: str | None
    national_dex_number: int | None


@dataclass(frozen=True, slots=True)
class DraftRoundView:
    round_number: int
    display_set: int
    reroll_available: bool
    legendary_selected: bool
    options: tuple[DraftOptionView, ...]


@dataclass(frozen=True, slots=True)
class DraftSelectionView:
    round_number: int
    pokemon_id: UUID
    pokemon_name: str
    team_slot: int
    draft_complete: bool
    legendary_selected: bool


class DraftService:
    """Transactional application use cases for presenting and resolving a draft."""

    def __init__(self, session: AsyncSession, policy: DraftProbabilityPolicy) -> None:
        self._session = session
        self._policy = policy

    async def get_current_round(self, *, owner: RunOwner, run_id: UUID) -> DraftRoundView:
        async with self._session.begin():
            run = await self._get_locked_draft_run(owner=owner, run_id=run_id)
            await self._sync_legendary_selection(run)
            round_number = await self._next_round_number(run_id)
            if round_number > DRAFT_ROUNDS:
                raise DraftCompleted("All six draft rounds have already been selected.")

            pending = await self._get_pending_round(run_id, round_number)
            if not pending:
                pending = await self._create_options(
                    run=run,
                    round_number=round_number,
                    display_set=0,
                )
            elif len(pending) != DRAFT_OPTIONS_PER_ROUND:
                raise DraftPoolConfigurationError(
                    "The current draft round must contain exactly six pending options."
                )
            return self._round_view(run, round_number, pending)

    async def reroll_current_round(
        self, *, owner: RunOwner, run_id: UUID
    ) -> DraftRoundView:
        async with self._session.begin():
            run = await self._get_locked_draft_run(owner=owner, run_id=run_id)
            await self._sync_legendary_selection(run)
            if run.reroll_used or REROLLS_PER_RUN == 0:
                raise RerollUnavailable("The run's one reroll has already been used.")

            round_number = await self._next_round_number(run_id)
            if round_number > DRAFT_ROUNDS:
                raise DraftCompleted("There is no draft round left to reroll.")

            current = await self._get_pending_round(run_id, round_number)
            if not current:
                raise RerollUnavailable("Generate the current round before rerolling it.")
            if len(current) != DRAFT_OPTIONS_PER_ROUND:
                raise DraftPoolConfigurationError(
                    "The current draft round must contain exactly six pending options."
                )
            if any(option.display_set == 1 for option, _ in current):
                raise RerollUnavailable("This round has already been rerolled.")

            for option, _ in current:
                option.resolution = "REROLLED"
            run.reroll_used = True
            rerolled = await self._create_options(
                run=run,
                round_number=round_number,
                display_set=1,
            )
            await self._session.flush()
            return self._round_view(run, round_number, rerolled)

    async def select_option(
        self,
        *,
        owner: RunOwner,
        run_id: UUID,
        option_number: int,
    ) -> DraftSelectionView:
        if not 1 <= option_number <= DRAFT_OPTIONS_PER_ROUND:
            raise InvalidDraftSelection("Option number must be between 1 and 6.")

        async with self._session.begin():
            run = await self._get_locked_draft_run(owner=owner, run_id=run_id)
            round_number = await self._next_round_number(run_id)
            if round_number > DRAFT_ROUNDS:
                raise DraftCompleted("All six draft rounds have already been selected.")

            pending = await self._get_pending_round(run_id, round_number)
            if len(pending) != DRAFT_OPTIONS_PER_ROUND:
                raise InvalidDraftSelection("The current draft round is not fully generated.")

            selected = next(
                (
                    (option, pokemon)
                    for option, pokemon in pending
                    if option.option_number == option_number
                ),
                None,
            )
            if selected is None:
                raise InvalidDraftSelection("That option is not available in the current round.")
            selected_option, selected_pokemon = selected

            is_rare = selected_pokemon.is_legendary or selected_pokemon.is_mythical
            await self._sync_legendary_selection(run)
            if is_rare and run.legendary_selected:
                raise InvalidDraftSelection(
                    "Não é possível ter mais de um lendário ou mítico no time."
                )

            build = await self._get_default_build(selected_pokemon.id)
            team = await self._get_or_create_team(run_id)
            await self._session.flush()
            self._session.add(
                TeamPokemon(
                    team_id=team.id,
                    pokemon_id=selected_pokemon.id,
                    pokemon_build_id=build.id,
                    slot_number=round_number,
                    build_snapshot=self._build_snapshot(selected_pokemon, build),
                )
            )

            for option, _ in pending:
                option.resolution = (
                    "SELECTED" if option.id == selected_option.id else "REJECTED"
                )
            if is_rare:
                run.legendary_selected = True
            if round_number == DRAFT_ROUNDS:
                run.stage = RunStage.GYM.value

            await self._session.flush()
            return DraftSelectionView(
                round_number=round_number,
                pokemon_id=selected_pokemon.id,
                pokemon_name=selected_pokemon.name,
                team_slot=round_number,
                draft_complete=round_number == DRAFT_ROUNDS,
                legendary_selected=run.legendary_selected,
            )

    async def _get_locked_draft_run(self, *, owner: RunOwner, run_id: UUID) -> Run:
        run = await self._session.scalar(
            select(Run)
            .where(Run.id == run_id, run_owner_condition(owner))
            .with_for_update()
        )
        if run is None:
            raise RunNotFound("Run was not found for this account.")
        if run.status != RunStatus.ACTIVE.value or run.stage != RunStage.DRAFT.value:
            raise DraftUnavailable("This run is not accepting draft actions.")
        return run

    async def _sync_legendary_selection(self, run: Run) -> None:
        if run.legendary_selected:
            return
        existing_rare = await self._session.scalar(
            select(Pokemon.id)
            .join(TeamPokemon, TeamPokemon.pokemon_id == Pokemon.id)
            .join(Team, Team.id == TeamPokemon.team_id)
            .where(
                Team.run_id == run.id,
                or_(Pokemon.is_legendary.is_(True), Pokemon.is_mythical.is_(True)),
            )
            .limit(1)
        )
        if existing_rare is not None:
            run.legendary_selected = True

    async def _next_round_number(self, run_id: UUID) -> int:
        selected_rounds = await self._session.scalars(
            select(RunDraftOption.round_number)
            .where(
                RunDraftOption.run_id == run_id,
                RunDraftOption.resolution == "SELECTED",
            )
            .distinct()
        )
        selected = set(selected_rounds.all())
        return next(
            (number for number in range(1, DRAFT_ROUNDS + 1) if number not in selected),
            DRAFT_ROUNDS + 1,
        )

    async def _get_pending_round(
        self, run_id: UUID, round_number: int
    ) -> list[tuple[RunDraftOption, Pokemon]]:
        rows = await self._session.execute(
            select(RunDraftOption, Pokemon)
            .join(Pokemon, Pokemon.id == RunDraftOption.pokemon_id)
            .where(
                RunDraftOption.run_id == run_id,
                RunDraftOption.round_number == round_number,
                RunDraftOption.resolution == "PENDING",
            )
            .order_by(RunDraftOption.option_number)
        )
        return list(rows.all())

    async def _create_options(
        self, *, run: Run, round_number: int, display_set: int
    ) -> list[tuple[RunDraftOption, Pokemon]]:
        already_offered_species = (
            select(func.lower(Pokemon.name))
            .join(RunDraftOption, RunDraftOption.pokemon_id == Pokemon.id)
            .where(RunDraftOption.run_id == run.id)
        )
        default_build_exists = (
            select(PokemonBuild.id)
            .where(PokemonBuild.pokemon_id == Pokemon.id, PokemonBuild.is_default.is_(True))
            .exists()
        )
        candidates = list(
            (
                await self._session.scalars(
                    select(Pokemon)
                    .where(
                        Pokemon.is_draft_eligible.is_(True),
                        or_(
                            Pokemon.draft_tier.in_(self._policy.tier_weights.keys()),
                            Pokemon.is_legendary.is_(True),
                            Pokemon.is_mythical.is_(True),
                        ),
                        func.lower(Pokemon.name).not_in(already_offered_species),
                        default_build_exists,
                    )
                    .order_by(Pokemon.id)
                )
            ).all()
        )

        pools: dict[str, list[Pokemon]] = defaultdict(list)
        for pokemon in candidates:
            if pokemon.is_legendary or pokemon.is_mythical:
                pools["legendary"].append(pokemon)
            elif pokemon.draft_tier is not None:
                effective_tier = self._effective_draft_tier(pokemon)
                pools[f"tier:{effective_tier}"].append(pokemon)

        available_keys = {
            key: weight
            for key, weight in self._selection_weights(run, pools).items()
            if weight > 0
        }
        if not available_keys:
            raise DraftPoolConfigurationError("No eligible Pokémon remain in the draft catalog.")
        available_pokemon_count = len(
            {
                pokemon.name.casefold()
                for key in available_keys
                for pokemon in pools[key]
            }
        )
        if available_pokemon_count < DRAFT_OPTIONS_PER_ROUND:
            raise DraftPoolConfigurationError(
                "At least six distinct eligible Pokémon are required to generate a round."
            )

        random_seed = run.random_seed
        if random_seed is None:
            random_seed = randbits(63)
            run.random_seed = random_seed
        seed_material = f"{random_seed}:{round_number}:{display_set}".encode("ascii")
        rng = Random(int.from_bytes(sha256(seed_material).digest(), "big"))

        generated: list[tuple[RunDraftOption, Pokemon]] = []
        for option_number in range(1, DRAFT_OPTIONS_PER_ROUND + 1):
            categories = list(available_keys)
            weights = [float(available_keys[key]) for key in categories]
            chosen_category = rng.choices(categories, weights=weights, k=1)[0]
            pool = pools[chosen_category]
            if not pool:
                raise DraftPoolConfigurationError(
                    f"Draft tier pool {chosen_category} has no eligible Pokémon."
                )
            pokemon = rng.choice(pool)
            selected_species = pokemon.name.casefold()
            for category, candidate_pool in pools.items():
                candidate_pool[:] = [
                    candidate
                    for candidate in candidate_pool
                    if candidate.name.casefold() != selected_species
                ]
                if not candidate_pool:
                    available_keys.pop(category, None)
            option = RunDraftOption(
                run_id=run.id,
                pokemon_id=pokemon.id,
                round_number=round_number,
                display_set=display_set,
                option_number=option_number,
                resolution="PENDING",
            )
            self._session.add(option)
            generated.append((option, pokemon))

        await self._session.flush()
        return generated

    @staticmethod
    def _effective_draft_tier(pokemon: Pokemon) -> int:
        """Apply a minimum rarity based on competitive viability and base stats."""
        tier = pokemon.draft_tier or 1
        if pokemon.is_pseudo_legendary:
            return max(tier, 5)

        competitive_tier_floors = {
            "AG": 5,
            "UBER": 5,
            "OU": 5,
            "(OU)": 5,
            "UUBL": 5,
            "UU": 4,
            "RUBL": 4,
            "RU": 3,
            "NUBL": 3,
        }
        competitive_tier = (pokemon.competitive_tier or "").upper()
        tier = max(tier, competitive_tier_floors.get(competitive_tier, tier))

        total_base_stats = sum(
            value
            for value in (pokemon.base_stats or {}).values()
            if isinstance(value, (int, float))
        )
        if total_base_stats >= 600:
            return max(tier, 5)
        if total_base_stats >= 550:
            return max(tier, 4)
        if total_base_stats >= 500:
            return max(tier, 3)
        return tier

    def _selection_weights(
        self, run: Run, pools: dict[str, list[Pokemon]]
    ) -> dict[str, Decimal]:
        tier_weights: dict[str, Decimal] = {
            f"tier:{tier}": weight for tier, weight in self._policy.tier_weights.items()
        }
        tier_weights = {
            key: value for key, value in tier_weights.items() if value > 0 and pools.get(key)
        }
        tier_total = sum(tier_weights.values(), Decimal("0"))
        if not tier_total:
            return {}

        if not run.legendary_selected and pools.get("legendary"):
            regular_total = Decimal("1") - LEGENDARY_OFFER_PROBABILITY
            weights = {
                key: value / tier_total * regular_total
                for key, value in tier_weights.items()
            }
            weights["legendary"] = LEGENDARY_OFFER_PROBABILITY
            return weights

        return {key: value / tier_total for key, value in tier_weights.items()}

    async def _get_default_build(self, pokemon_id: UUID) -> PokemonBuild:
        builds = list(
            (
                await self._session.scalars(
                    select(PokemonBuild)
                    .where(
                        PokemonBuild.pokemon_id == pokemon_id,
                        PokemonBuild.is_default.is_(True),
                    )
                    .with_for_update()
                )
            ).all()
        )
        if len(builds) != 1:
            raise DraftPoolConfigurationError(
                "Each draft-eligible Pokémon must have exactly one default build."
            )
        return builds[0]

    async def _get_or_create_team(self, run_id: UUID) -> Team:
        team = await self._session.scalar(
            select(Team).where(Team.run_id == run_id).with_for_update()
        )
        if team is None:
            team = Team(run_id=run_id)
            self._session.add(team)
            await self._session.flush()
        return team

    def _round_view(
        self,
        run: Run,
        round_number: int,
        rows: list[tuple[RunDraftOption, Pokemon]],
    ) -> DraftRoundView:
        display_set = rows[0][0].display_set
        return DraftRoundView(
            round_number=round_number,
            display_set=display_set,
            reroll_available=not run.reroll_used,
            legendary_selected=run.legendary_selected,
            options=tuple(
                DraftOptionView(
                    option_number=option.option_number,
                    pokemon_id=pokemon.id,
                    name=pokemon.name,
                    form_name=pokemon.form_name,
                    primary_type=pokemon.primary_type,
                    secondary_type=pokemon.secondary_type,
                    draft_tier=self._effective_draft_tier(pokemon),
                    is_legendary=pokemon.is_legendary,
                    is_mythical=pokemon.is_mythical,
                    is_pseudo_legendary=pokemon.is_pseudo_legendary,
                    front_sprite_url=pokemon.front_sprite_url,
                    national_dex_number=pokemon.national_dex_number,
                )
                for option, pokemon in rows
            ),
        )

    @staticmethod
    def _build_snapshot(pokemon: Pokemon, build: PokemonBuild) -> dict[str, object]:
        return {
            "pokemon_external_key": pokemon.external_key,
            "pokemon_name": pokemon.name,
            "pokemon_form": pokemon.form_name,
            "build_key": build.build_key,
            "nature": build.nature,
            "ability": build.ability,
            "held_item": build.held_item,
            "moves": build.moves,
            "evs": build.evs,
            "ivs": build.ivs,
        }
