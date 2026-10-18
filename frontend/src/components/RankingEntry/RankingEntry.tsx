import { FaMedal } from 'react-icons/fa6'
import { TbPokeball } from 'react-icons/tb'
import PokemonSprite from '../PokemonSprite/PokemonSprite'
import type { ChampionRankingEntry as ChampionRankingEntryData } from '../../types/championship'

type RankingEntryProps = {
  entry: ChampionRankingEntryData
  position: number
}

const medalColors = {
  1: 'text-[#bc8c24]',
  2: 'text-[#87939b]',
  3: 'text-[#b76a38]',
}

export default function RankingEntry({ entry, position }: RankingEntryProps) {
  const medalColor = medalColors[position as keyof typeof medalColors]

  return (
    <li>
      <article
        className={`grid grid-cols-[3.5rem_minmax(0,1fr)] items-center gap-x-3 gap-y-1 border-2 px-2.5 py-2.5 sm:px-4 xl:grid-cols-[4.5rem_15rem_minmax(0,1fr)_6.5rem] xl:gap-x-4 xl:py-2 ${
          position === 1
            ? 'border-[#d3a844] bg-[#fff2cd]'
            : position === 2
              ? 'border-[#cbd1d5] bg-[#f0f1ef]'
              : position === 3
                ? 'border-[#e1b99b] bg-[#fff1e5]'
                : 'border-[#dedbd2] bg-[#fffdf7]'
        }`}
      >
        <div className="row-span-3 flex items-center justify-center font-display text-2xl text-[#102f5b] xl:row-span-1">
          {medalColor ? (
            <span className="relative grid size-12 place-items-center">
              <FaMedal aria-hidden="true" className={`absolute inset-0 size-12 ${medalColor}`} />
              <span className="relative z-10 text-lg text-[#fffaf0] drop-shadow-[0_1px_1px_#102f5b]">{position}</span>
            </span>
          ) : (
            <span>{position}</span>
          )}
        </div>

        <div className="flex min-w-0 items-center gap-2 xl:col-start-2">
          <span aria-hidden="true" className="grid size-10 shrink-0 place-items-center rounded-full border-2 border-[#102f5b]/20 bg-paper text-brand-strong">
            <TbPokeball className="text-2xl" />
          </span>
          <span className="min-w-0 whitespace-normal break-words border border-[#102f5b]/15 bg-white/70 px-2.5 py-1 font-display text-base font-bold uppercase leading-tight tracking-wide text-[#102f5b] shadow-[0_2px_0_rgba(16,47,91,0.1)] sm:px-3 sm:text-lg">{entry.trainer_name}</span>
        </div>

        <ul aria-label={`Time de ${entry.trainer_name}`} className="col-start-2 row-start-2 m-0 grid min-w-0 list-none grid-cols-3 items-center justify-items-center gap-x-1 gap-y-0 p-0 md:grid-cols-6 md:gap-x-2 xl:col-start-3 xl:row-start-1 xl:flex xl:justify-start xl:gap-3">
          {entry.team.slice(0, 6).map((pokemon, index) => (
            <li key={`${pokemon.pokemon_id}-${index}`} className="grid min-w-0 place-items-center xl:flex-none" title={pokemon.pokemon_name}>
              <PokemonSprite
                name={pokemon.pokemon_name}
                pokedexNumber={pokemon.national_dex_number ?? undefined}
                size="compact"
                spriteUrl={pokemon.front_sprite_url}
              />
            </li>
          ))}
          {entry.team.length === 0 && <li className="text-sm text-[#536987]">Time indisponível</li>}
        </ul>

        <div className="col-start-2 row-start-3 flex items-center justify-between gap-2 xl:col-start-4 xl:row-start-1 xl:flex-col xl:items-end xl:justify-center xl:gap-0">
          <span className="font-display text-lg leading-none text-[#102f5b] sm:text-xl">{entry.completed_battles}/13</span>
          <span className="font-display text-xs uppercase leading-none text-brand-strong sm:text-sm">Campeão</span>
        </div>
      </article>
    </li>
  )
}
