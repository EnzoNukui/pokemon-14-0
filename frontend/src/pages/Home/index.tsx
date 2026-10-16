import { FaChevronRight } from 'react-icons/fa'
import { TbPokeball } from 'react-icons/tb'
import { Link } from 'react-router'
import ActionLink from '../../components/ActionLink/ActionLink'
import PokemonSprite from '../../components/PokemonSprite/PokemonSprite'
import PokemonTeam from '../../components/PokemonTeam/PokemonTeam'
import RunProgress from '../../components/RunProgress/RunProgress'
import { ROUTES } from '../../routes/paths'

type ChampionSummary = {
  trainer: string
  completedAt: string
  team: { name: string; pokedexNumber: number }[]
}

const latestChampion: ChampionSummary | null = null

export default function HomePage() {
  return (
    <div className="pb-10 sm:pb-14">
      <section className="mx-auto grid w-full max-w-[90rem] grid-cols-1 items-center gap-9 px-4 py-10 sm:px-8 sm:py-12 lg:grid-cols-[1fr_1fr] lg:gap-12 lg:py-14">
        <div className="min-w-0">
          <div className="mb-4 flex items-center gap-3 text-brand-strong sm:mb-5 sm:gap-4">
            <TbPokeball aria-hidden="true" className="shrink-0 text-4xl" />
            <span className="whitespace-nowrap font-[Impact,Arial_Narrow,sans-serif] text-base uppercase tracking-wide sm:text-xl">
              Desafio de treinador
            </span>
            <span aria-hidden="true" className="h-0.5 min-w-5 flex-1 bg-brand" />
            <TbPokeball aria-hidden="true" className="shrink-0 text-3xl" />
          </div>

          <h1 className="m-0 !font-[Impact,Arial_Narrow,sans-serif] text-5xl uppercase leading-[0.94] tracking-tight text-[#102f5b] sm:text-6xl xl:text-7xl">
            <span className="block">Monte seu time.</span>
            <span className="mt-1 block text-brand">Vença 14 batalhas.</span>
          </h1>

          <p className="mb-0 mt-4 max-w-xl font-sans text-lg leading-snug text-[#28649a] sm:mt-5 sm:text-xl">
            Escolha 6 Pokémon e enfrente 14 treinadores até se tornar o novo campeão.
          </p>

          <div className="mt-6 flex flex-wrap items-center gap-x-6 gap-y-3 sm:mt-8">
            <ActionLink to={ROUTES.play}>
              Começar run
              <FaChevronRight aria-hidden="true" className="text-sm" />
            </ActionLink>
            <ActionLink to={ROUTES.play} variant="secondary">
              Como funciona
              <FaChevronRight aria-hidden="true" className="text-sm" />
            </ActionLink>
          </div>
        </div>

        <PokemonTeam />
      </section>

      <RunProgress />

      <section
        aria-labelledby="last-champion-heading"
        className="mx-auto mt-6 w-full max-w-[90rem] border-y border-[#24639a] px-4 py-5 sm:mt-8 sm:px-8 sm:py-6"
      >
        <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:gap-0">
          <div className="flex items-center gap-3 border-b border-[#102f5b]/30 pb-4 lg:w-[24%] lg:border-b-0 lg:border-r lg:pb-0 lg:pr-5">
            <TbPokeball aria-hidden="true" className="shrink-0 text-3xl text-brand" />
            <div>
              <h2
                id="last-champion-heading"
                className="m-0 font-[Impact,Arial_Narrow,sans-serif] text-xl uppercase leading-none text-[#102f5b] sm:text-2xl"
              >
                Último campeão
              </h2>
              <p className="mb-0 mt-1 text-sm leading-snug text-[#28649a] sm:text-base">
                Veja quem concluiu o desafio mais recentemente.
              </p>
            </div>
          </div>

          {latestChampion && (
            <>
              <div className="flex flex-col justify-center border-b border-[#102f5b]/30 pb-4 sm:flex-row sm:items-center sm:justify-between lg:w-[20%] lg:border-b-0 lg:px-6 lg:pb-0">
                <p className="m-0 font-[Impact,Arial_Narrow,sans-serif] text-2xl leading-none text-[#102f5b]">
                  {latestChampion.trainer}
                </p>
                <p className="mb-0 mt-1 text-sm text-[#28649a] sm:mt-0 sm:text-right">
                  Campeão em {latestChampion.completedAt}
                </p>
              </div>

              <ul
                aria-label="Time do último campeão"
                className="m-0 grid list-none grid-cols-3 gap-x-2 gap-y-3 sm:grid-cols-6 lg:flex lg:flex-1 lg:justify-center lg:gap-3 lg:px-4"
              >
                {latestChampion.team.map((pokemon) => (
                  <li
                    key={pokemon.name}
                    className="flex min-w-0 flex-col items-center justify-end text-center text-xs text-[#28649a] sm:text-sm"
                  >
                    <PokemonSprite name={pokemon.name} pokedexNumber={pokemon.pokedexNumber} size="compact" />
                    <span className="mt-0.5">{pokemon.name}</span>
                  </li>
                ))}
              </ul>
            </>
          )}

          <div className="flex justify-end border-t border-[#102f5b]/30 pt-4 lg:ml-3 lg:border-l lg:border-t-0 lg:pl-6 lg:pt-0">
            <Link
              to={ROUTES.hallOfFame}
              className="inline-flex items-center gap-2 font-[Impact,Arial_Narrow,sans-serif] text-lg uppercase text-[#102f5b] underline decoration-2 underline-offset-4 hover:text-brand-strong"
            >
              Ver ranking
              <FaChevronRight aria-hidden="true" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
