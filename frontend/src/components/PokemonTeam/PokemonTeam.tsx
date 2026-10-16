import { TbPokeball } from 'react-icons/tb'
import PokemonSprite from '../PokemonSprite/PokemonSprite'

export const sampleTeam = [
  { name: 'Charizard', pokedexNumber: 6 },
  { name: 'Lapras', pokedexNumber: 131 },
  { name: 'Snorlax', pokedexNumber: 143 },
  { name: 'Alakazam', pokedexNumber: 65 },
  { name: 'Jolteon', pokedexNumber: 135 },
  { name: 'Gyarados', pokedexNumber: 130 },
]

export default function PokemonTeam() {
  return (
    <section
      aria-label="Exemplo de time Pokémon para uma run"
      className="overflow-hidden rounded-2xl border-[3px] border-[#102f5b] bg-white p-2 shadow-[inset_0_0_0_3px_#d7e3ec] sm:p-3"
    >
      <div className="flex min-h-14 items-center justify-between gap-3 rounded-t-lg bg-brand px-3 py-2 text-white sm:px-5">
        <div className="flex min-w-0 items-center gap-2.5 sm:gap-4">
          <TbPokeball aria-hidden="true" className="shrink-0 text-3xl" />
          <h2 className="m-0 whitespace-nowrap !font-[Impact,Arial_Narrow,sans-serif] text-base uppercase leading-none sm:text-xl">
            Seu time na run
          </h2>
        </div>
        <span className="shrink-0 rounded-md border-2 border-[#102f5b] bg-white px-3 py-1 font-[Impact,Arial_Narrow,sans-serif] text-lg leading-none text-[#102f5b] sm:px-4 sm:text-xl">
          0/6
        </span>
      </div>

      <ul className="m-0 grid list-none grid-cols-3 gap-2 p-2 sm:gap-3 sm:p-3">
        {sampleTeam.map((pokemon) => (
          <li
            key={pokemon.name}
            className="relative grid aspect-[1.06/1] place-items-center overflow-hidden rounded-lg border-2 border-[#102f5b] bg-[#fffefa]"
          >
            <span aria-hidden="true" className="absolute bottom-4 h-4 w-20 rounded-[50%] bg-graphite/10" />
            <PokemonSprite name={pokemon.name} pokedexNumber={pokemon.pokedexNumber} />
          </li>
        ))}
      </ul>
    </section>
  )
}
