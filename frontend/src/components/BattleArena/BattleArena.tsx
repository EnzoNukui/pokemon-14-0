import { useMemo } from 'react'
import PokemonSprite from '../PokemonSprite/PokemonSprite'
import type { BattleEvent, BattlePokemon } from '../../types/battle'
import type { RunTeamMember } from '../../types/run'

type BattleArenaProps = {
  battleNumber: number
  trainerName: string
  trainerSpriteUrl: string | null
  playerTeam: RunTeamMember[]
  opponentTeam: BattlePokemon[]
  events: BattleEvent[]
}

type SceneState = {
  playerName: string
  opponentName: string
  playerCondition?: string
  opponentCondition?: string
  playerIndex: number | null
  opponentIndex: number | null
  faintedPlayer: Set<number>
  faintedOpponent: Set<number>
}

type TeamPokemon = RunTeamMember | BattlePokemon

function pokemonName(pokemon: TeamPokemon): string {
  return 'pokemon_name' in pokemon ? pokemon.pokemon_name : pokemon.name
}

function nameFromIdent(ident: string): string {
  return ident.replace(/^p[12][a-z]:\s*/i, '').trim()
}

function sideFromIdent(ident: string): 'player' | 'opponent' | null {
  if (ident.startsWith('p1')) return 'player'
  if (ident.startsWith('p2')) return 'opponent'
  return null
}

function normalizeName(name: string): string {
  return name.toLocaleLowerCase().replace(/[^a-z0-9]/g, '')
}

function eventParts(event: BattleEvent): string[] {
  const parts = event.payload.parts
  return Array.isArray(parts) ? parts.filter((part): part is string => typeof part === 'string') : []
}

function findTeamIndex(
  team: TeamPokemon[],
  name: string,
  activeIndex: number | null,
  fainted: Set<number>,
): number | null {
  const normalizedName = normalizeName(name)
  const matchingIndexes = team.flatMap((pokemon, index) =>
    normalizeName(pokemonName(pokemon)) === normalizedName ? [index] : [],
  )
  if (matchingIndexes.length === 0) return null

  const availableIndexes = matchingIndexes.filter((index) => !fainted.has(index))
  // A switch event for a duplicate species represents another team slot when
  // that species is already active; the event ident itself only carries its name.
  if (activeIndex !== null && matchingIndexes.includes(activeIndex)) {
    const otherAvailableIndex = availableIndexes.find((index) => index !== activeIndex)
    if (otherAvailableIndex !== undefined) return otherAvailableIndex
    if (availableIndexes.includes(activeIndex)) return activeIndex
  }

  return availableIndexes[0] ?? matchingIndexes[0]
}

function createSceneState(
  playerTeam: RunTeamMember[],
  opponentTeam: BattlePokemon[],
  events: BattleEvent[],
): SceneState {
  const state: SceneState = {
    playerName: playerTeam[0]?.pokemon_name ?? 'Seu Pokémon',
    opponentName: opponentTeam[0]?.name ?? 'Pokémon adversário',
    playerIndex: null,
    opponentIndex: null,
    faintedPlayer: new Set(),
    faintedOpponent: new Set(),
  }

  for (const event of events) {
    const parts = eventParts(event)
    const ident = parts[0]
    if (!ident) continue
    const side = sideFromIdent(ident)
    if (!side) continue
    const name = nameFromIdent(ident)

    if (event.event_type === 'switch' || event.event_type === 'drag') {
      if (side === 'player') {
        state.playerName = name
        state.playerIndex = findTeamIndex(playerTeam, name, state.playerIndex, state.faintedPlayer)
      } else {
        state.opponentName = name
        state.opponentIndex = findTeamIndex(opponentTeam, name, state.opponentIndex, state.faintedOpponent)
      }
      const condition = parts[2]
      if (condition) {
        if (side === 'player') state.playerCondition = condition
        else state.opponentCondition = condition
      }
    }

    if (event.event_type === '-damage' || event.event_type === '-heal' || event.event_type === '-sethp') {
      const condition = parts[1]
      if (condition) {
        if (side === 'player') state.playerCondition = condition
        else state.opponentCondition = condition
      }
    }

    if (event.event_type === 'faint') {
      const fainted = side === 'player' ? state.faintedPlayer : state.faintedOpponent
      const activeIndex = side === 'player' ? state.playerIndex : state.opponentIndex
      const team = side === 'player' ? playerTeam : opponentTeam
      const faintedIndex = activeIndex ?? findTeamIndex(team, name, null, fainted)
      if (faintedIndex !== null) fainted.add(faintedIndex)
      if (side === 'player') state.playerCondition = '0 fnt'
      else state.opponentCondition = '0 fnt'
    }
  }

  return state
}

function HealthBar({ condition }: { condition?: string }) {
  if (!condition) return <div aria-hidden="true" className="mt-1 h-2.5 w-full rounded-full bg-graphite/15" />
  const match = condition.match(/^(\d+(?:\.\d+)?)\s*\/\s*(\d+(?:\.\d+)?)/)
  if (!match) return <span className="mt-1 block font-display text-[0.62rem] uppercase text-danger">Nocauteado</span>
  const current = Number(match[1])
  const maximum = Number(match[2])
  const percentage = maximum > 0 ? Math.max(0, Math.min(100, (current / maximum) * 100)) : 0

  return (
    <div className="mt-1 w-full">
      <div aria-label={`HP ${Math.round(percentage)}%`} aria-valuemax={100} aria-valuemin={0} aria-valuenow={Math.round(percentage)} className="h-2.5 overflow-hidden rounded-full border border-graphite/30 bg-[#d9d6c9] p-[1px]" role="progressbar">
        <span className={`block h-full rounded-full transition-[width] duration-500 ${percentage <= 25 ? 'bg-danger' : percentage <= 50 ? 'bg-[#d09a32]' : 'bg-[#5a9c58]'}`} style={{ width: `${percentage}%` }} />
      </div>
      <span className="mt-0.5 block text-right font-display text-[0.58rem] text-graphite-muted">{current} / {maximum} HP</span>
    </div>
  )
}

function StatusCard({ name, condition, align = 'left' }: { name: string; condition?: string; align?: 'left' | 'right' }) {
  return (
    <section className={`w-full max-w-[19rem] border-[3px] border-graphite bg-paper px-3 py-2 shadow-[3px_3px_0_#7d8f70] sm:px-4 ${align === 'right' ? 'ml-auto' : ''}`}>
      <h2 className="m-0 truncate font-display text-base uppercase text-graphite sm:text-lg">{name}</h2>
      <HealthBar condition={condition} />
    </section>
  )
}

function TeamStrip({
  team,
  activeName,
  activeIndex,
  fainted,
  side,
}: {
  team: RunTeamMember[] | BattlePokemon[]
  activeName: string
  activeIndex: number | null
  fainted: Set<number>
  side: 'player' | 'opponent'
}) {
  return (
    <ol aria-label={side === 'player' ? 'Seu time' : 'Time adversário'} className="m-0 flex list-none items-center gap-1 p-0 sm:gap-1.5">
      {team.map((pokemon, index) => {
        const name = pokemonName(pokemon)
        const isFainted = fainted.has(index)
        const dexNumber = pokemon.national_dex_number ?? undefined
        const spriteUrl = pokemon.front_sprite_url
        const selected = activeIndex === index || (activeIndex === null && normalizeName(activeName) === normalizeName(name))
        return (
          <li key={`${pokemon.pokemon_id}-${index}`} aria-label={`${name}${isFainted ? ', nocauteado' : ''}`} className={`grid size-8 shrink-0 place-items-center border-2 bg-paper sm:size-12 ${selected ? 'border-brand-strong' : 'border-graphite/25'} ${isFainted ? 'opacity-35 grayscale' : ''}`}>
            <PokemonSprite name={name} pokedexNumber={dexNumber} spriteUrl={spriteUrl} size="team" />
          </li>
        )
      })}
    </ol>
  )
}

export default function BattleArena({
  battleNumber,
  trainerName,
  trainerSpriteUrl,
  playerTeam,
  opponentTeam,
  events,
}: BattleArenaProps) {
  const state = useMemo(() => createSceneState(playerTeam, opponentTeam, events), [events, opponentTeam, playerTeam])
  const player = playerTeam[state.playerIndex ?? 0]
  const opponent = opponentTeam[state.opponentIndex ?? 0]

  return (
    <section aria-label="Arena da batalha" className="overflow-hidden border-[3px] border-graphite bg-paper shadow-[4px_4px_0_rgb(53_53_58_/_18%)]">
      <header className="flex items-center justify-between border-b-[3px] border-graphite bg-surface px-4 py-2">
        <p className="m-0 font-display text-sm uppercase text-graphite sm:text-base">Desafio Pokémon</p>
        <span className="border-2 border-graphite/60 bg-paper px-2 py-1 font-display text-xs uppercase text-graphite sm:text-sm">Batalha {String(battleNumber).padStart(2, '0')} / 13</span>
      </header>

      <div className="relative min-h-[27rem] overflow-hidden bg-[linear-gradient(180deg,#9d95bb_0%,#8e87ae_44%,#45675a_44%,#3d5d52_100%)] sm:min-h-[32rem]">
        <div aria-hidden="true" className="absolute inset-x-0 top-[8%] h-[12%] bg-[#b2a9cc]/35" />
        <div aria-hidden="true" className="absolute inset-x-0 top-[22%] h-[11%] bg-[#827ba5]/30" />
        <div aria-hidden="true" className="absolute inset-x-0 top-[42%] h-[3%] bg-[#a69fc2]/25" />
        <div aria-hidden="true" className="absolute inset-x-0 bottom-0 top-[45%] bg-[repeating-linear-gradient(180deg,rgba(139,171,143,0.13)_0,rgba(139,171,143,0.13)_7px,transparent_8px,transparent_38px)]" />
        <div aria-hidden="true" className="absolute inset-x-0 top-[44%] h-1 border-y border-[#263f38]/55 bg-[#2d4a40]/80" />

        <div aria-hidden="true" className="absolute left-[53%] top-[48%] h-12 w-[34%] -translate-x-1/2 rounded-[48%_52%_43%_57%/51%_45%_55%_49%] border-[3px] border-[#263f38]/75 bg-[#7d6b78] shadow-[0_5px_0_rgb(31_49_43_/_35%)] sm:left-[62%] sm:top-[47%] sm:h-16 sm:w-[31%]">
          <span className="absolute inset-[5px] rounded-[48%_52%_43%_57%/51%_45%_55%_49%] bg-[#98818b]" />
          <span className="absolute inset-x-[18%] top-[35%] h-[28%] rounded-full bg-[#ad9698]/75" />
        </div>
        <div aria-hidden="true" className="absolute left-[26%] top-[83%] h-14 w-[39%] -translate-x-1/2 rounded-[55%_45%_52%_48%/45%_53%_47%_55%] border-[3px] border-[#263f38]/75 bg-[#766771] shadow-[0_5px_0_rgb(31_49_43_/_35%)] sm:left-[18%] sm:top-[82%] sm:h-[4.5rem] sm:w-[36%]">
          <span className="absolute inset-[5px] rounded-[55%_45%_52%_48%/45%_53%_47%_55%] bg-[#95808a]" />
          <span className="absolute inset-x-[19%] top-[34%] h-[27%] rounded-full bg-[#aa9395]/70" />
        </div>

        <div className="absolute left-3 right-3 top-4 z-20 sm:left-6 sm:right-6 sm:top-5">
          <StatusCard name={`${trainerName} · ${state.opponentName}`} condition={state.opponentCondition} />
        </div>

        {trainerSpriteUrl && (
          <img alt={`Treinador ${trainerName}`} className="absolute right-2 top-[5.5rem] z-10 h-28 w-24 object-contain [image-rendering:pixelated] sm:right-[4%] sm:top-24 sm:h-44 sm:w-36" decoding="async" src={trainerSpriteUrl} />
        )}

        {opponent && (
          <div className="absolute right-[26%] top-[19%] z-10 flex h-36 w-36 items-center justify-center sm:right-[29%] sm:top-[16%] sm:h-56 sm:w-56">
            <span aria-hidden="true" className="absolute bottom-3 left-1/2 h-7 w-28 -translate-x-1/2 rounded-[50%] bg-graphite/15 blur-sm sm:bottom-5 sm:h-10 sm:w-40" />
            <PokemonSprite name={opponent.name} pokedexNumber={opponent.national_dex_number ?? undefined} spriteUrl={opponent.front_sprite_url} size="battle" />
          </div>
        )}

        {player && (
          <div className="absolute bottom-0 left-[3%] z-10 flex h-44 w-44 items-end justify-center sm:bottom-1 sm:left-[8%] sm:h-64 sm:w-64">
            <span aria-hidden="true" className="absolute bottom-2 left-1/2 h-8 w-36 -translate-x-1/2 rounded-[50%] bg-graphite/15 blur-sm sm:bottom-3 sm:h-11 sm:w-52" />
            <PokemonSprite name={player.pokemon_name} pokedexNumber={player.national_dex_number ?? undefined} spriteUrl={player.back_sprite_url} side="back" size="battle" />
          </div>
        )}

        <div className="absolute bottom-3 right-3 z-20 flex w-[68%] flex-col items-end gap-1 sm:bottom-5 sm:right-6 sm:w-[43%] sm:gap-1.5">
          <StatusCard align="right" name={state.playerName} condition={state.playerCondition} />
          <TeamStrip team={playerTeam} activeName={state.playerName} activeIndex={state.playerIndex} fainted={state.faintedPlayer} side="player" />
        </div>

        <div className="absolute left-3 top-[5.8rem] z-20 sm:left-6 sm:top-[6.5rem]">
          <TeamStrip team={opponentTeam} activeName={state.opponentName} activeIndex={state.opponentIndex} fainted={state.faintedOpponent} side="opponent" />
        </div>
      </div>
    </section>
  )
}
