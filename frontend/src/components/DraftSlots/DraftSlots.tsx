import PokemonSprite from '../PokemonSprite/PokemonSprite'
import type { RunTeamMember } from '../../types/run'

type DraftSlotsProps = {
  team: RunTeamMember[]
}

export default function DraftSlots({ team }: DraftSlotsProps) {
  const membersBySlot = new Map(team.map((member) => [member.slot_number, member]))

  return (
    <ol aria-label="Pokémon escolhidos para a run" className="m-0 grid list-none grid-cols-3 justify-items-center gap-x-4 gap-y-3 p-0 sm:grid-cols-6 sm:gap-x-5 lg:gap-x-7">
      {Array.from({ length: 6 }, (_, index) => {
        const slotNumber = index + 1
        const member = membersBySlot.get(slotNumber)

        return (
          <li key={slotNumber}>
            <div
              aria-label={member ? `${member.pokemon_name} no espaço ${slotNumber}` : `Espaço ${slotNumber} vazio`}
              role="img"
              className={`grid size-[4.5rem] place-items-center rounded-full border-[3px] bg-surface-muted sm:size-[5.25rem] md:size-[5.75rem] ${member ? 'border-brand-strong' : 'border-dashed border-graphite/70'}`}
            >
              {member ? (
                <PokemonSprite
                  name={member.pokemon_name}
                  pokedexNumber={member.national_dex_number ?? undefined}
                  spriteUrl={member.front_sprite_url}
                  size="compact"
                />
              ) : (
                <span aria-hidden="true" className="size-2 rounded-full bg-graphite/15" />
              )}
            </div>
          </li>
        )
      })}
    </ol>
  )
}
