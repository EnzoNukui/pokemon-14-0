"""HTTP schemas for the Pokémon draft."""

from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.runs.application.draft_service import (
    DraftOptionView,
    DraftRoundView,
    DraftSelectionView,
)


class DraftOptionResponse(BaseModel):
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

    @classmethod
    def from_view(cls, view: DraftOptionView) -> "DraftOptionResponse":
        return cls(
            option_number=view.option_number,
            pokemon_id=view.pokemon_id,
            name=view.name,
            form_name=view.form_name,
            primary_type=view.primary_type,
            secondary_type=view.secondary_type,
            draft_tier=view.draft_tier,
            is_legendary=view.is_legendary,
            is_mythical=view.is_mythical,
            is_pseudo_legendary=view.is_pseudo_legendary,
            front_sprite_url=view.front_sprite_url,
        )


class DraftRoundResponse(BaseModel):
    round_number: int
    display_set: int
    reroll_available: bool
    options: list[DraftOptionResponse]

    @classmethod
    def from_view(cls, view: DraftRoundView) -> "DraftRoundResponse":
        return cls(
            round_number=view.round_number,
            display_set=view.display_set,
            reroll_available=view.reroll_available,
            options=[DraftOptionResponse.from_view(option) for option in view.options],
        )


class SelectDraftOptionRequest(BaseModel):
    option_number: int = Field(ge=1, le=6)


class DraftSelectionResponse(BaseModel):
    round_number: int
    pokemon_id: UUID
    pokemon_name: str
    team_slot: int
    draft_complete: bool
    legendary_selected: bool

    @classmethod
    def from_view(cls, view: DraftSelectionView) -> "DraftSelectionResponse":
        return cls(
            round_number=view.round_number,
            pokemon_id=view.pokemon_id,
            pokemon_name=view.pokemon_name,
            team_slot=view.team_slot,
            draft_complete=view.draft_complete,
            legendary_selected=view.legendary_selected,
        )
