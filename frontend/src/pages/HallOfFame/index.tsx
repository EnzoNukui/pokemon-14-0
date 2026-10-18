import { useEffect, useState } from 'react'
import { FaTrophy } from 'react-icons/fa6'
import { TbPokeball } from 'react-icons/tb'
import { Link, useLocation } from 'react-router'
import RankingEntry from '../../components/RankingEntry/RankingEntry'
import useAuth from '../../components/AuthProvider/useAuth'
import { championRankingPreview } from '../../data/championRankingPreview'
import { ROUTES } from '../../routes/paths'
import { getChampionRanking } from '../../service/championshipService'
import type { ChampionRankingEntry } from '../../types/championship'

export default function HallOfFamePage() {
  const { session } = useAuth()
  const location = useLocation()
  const isPreview = new URLSearchParams(location.search).get('preview') === 'ranking'
  const [champions, setChampions] = useState<ChampionRankingEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)
  const displayedChampions = isPreview ? championRankingPreview : champions

  useEffect(() => {
    if (isPreview) return

    let cancelled = false
    getChampionRanking(5)
      .then((ranking) => {
        if (!cancelled) setChampions(ranking)
      })
      .catch(() => {
        if (!cancelled) setError(true)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => { cancelled = true }
  }, [isPreview])

  return (
    <div className="pb-10 sm:pb-14">
      <section aria-labelledby="ranking-title" className="mx-auto w-full max-w-[90rem] px-4 pb-6 pt-8 text-center sm:px-8 sm:pb-8 sm:pt-10">
        <FaTrophy aria-hidden="true" className="mx-auto text-5xl text-[#bd8b28] drop-shadow-[0_3px_0_#102f5b] sm:text-6xl" />
        <h1 id="ranking-title" className="m-0 mt-3 font-display text-3xl uppercase leading-none text-[#102f5b] sm:text-5xl lg:text-6xl">
          Ranking de campeões
        </h1>
        <div className="mx-auto mt-3 flex max-w-2xl items-center justify-center gap-3 text-[#102f5b] sm:gap-4">
          <span aria-hidden="true" className="h-0.5 min-w-6 flex-1 bg-[#102f5b]/40" />
          <TbPokeball aria-hidden="true" className="shrink-0 text-xl text-brand-strong" />
          <p className="m-0 font-display text-sm sm:text-lg">As maiores jornadas da Liga</p>
          <TbPokeball aria-hidden="true" className="shrink-0 text-xl text-brand-strong" />
          <span aria-hidden="true" className="h-0.5 min-w-6 flex-1 bg-[#102f5b]/40" />
        </div>
      </section>

      <div className="mx-auto grid w-full max-w-[90rem] grid-cols-1 gap-5 px-4 sm:px-8 min-[1400px]:grid-cols-[minmax(0,1fr)_18rem] min-[1400px]:gap-6">
        <section aria-label="Treinadores campeões" className="min-w-0 overflow-hidden border-[3px] border-[#102f5b] bg-surface shadow-[0_4px_0_#102f5b]">
          <div className="hidden grid-cols-[4.5rem_15rem_minmax(0,1fr)_6.5rem] items-center gap-4 border-b-2 border-[#102f5b]/20 bg-[#e8e6e0] px-4 py-3 font-display text-xs uppercase tracking-wide text-[#102f5b] xl:grid">
            <span>Posição</span>
            <span>Treinador</span>
            <span>Equipe</span>
            <span className="text-right">Resultado</span>
          </div>

          {(!isPreview && loading) ? (
            <p aria-live="polite" className="m-0 px-4 py-12 text-center font-display uppercase text-[#536987]">Carregando ranking…</p>
          ) : (!isPreview && error) ? (
            <p aria-live="polite" className="m-0 px-4 py-12 text-center text-sm text-[#536987]">Não foi possível carregar o ranking agora. Tente novamente em instantes.</p>
          ) : displayedChampions.length === 0 ? (
            <div className="px-4 py-12 text-center">
              <TbPokeball aria-hidden="true" className="mx-auto text-4xl text-brand" />
              <p className="mb-0 mt-2 font-display uppercase text-[#102f5b]">Ainda não há campeões no ranking.</p>
              <p className="mb-0 mt-1 text-sm text-[#536987]">Conclua uma jornada para entrar na Liga.</p>
            </div>
          ) : (
            <ol aria-label="Top 5 campeões" className="m-0 grid list-none gap-2 p-2 sm:gap-2.5 sm:p-3">
              {displayedChampions.map((entry, index) => (
                <RankingEntry key={entry.id} entry={entry} position={index + 1} />
              ))}
            </ol>
          )}
        </section>

        <aside aria-labelledby="journey-title" className="self-start border-[3px] border-[#102f5b] bg-surface shadow-[0_4px_0_#102f5b]">
          <h2 id="journey-title" className="m-0 border-b-2 border-[#102f5b]/20 bg-[#e8e6e0] px-4 py-3 text-center font-display text-lg uppercase text-[#102f5b]">
            Sua jornada
          </h2>
          <div className="flex flex-col items-center px-5 py-5 text-center">
            <span aria-hidden="true" className="grid size-20 place-items-center rounded-full border-[3px] border-[#102f5b] bg-brand-soft text-brand-strong shadow-[inset_0_0_0_5px_#fffaf0]">
              <TbPokeball className="text-5xl" />
            </span>
            {session ? (
              <>
                <p className="mb-0 mt-3 font-display text-lg uppercase text-[#102f5b]">Olá, {session.user.trainer_name}</p>
                <p className="mb-0 mt-1 text-sm leading-snug text-[#536987]">Sua próxima jornada pode entrar para o ranking.</p>
                <Link className="mt-4 inline-flex min-h-12 w-full items-center justify-center border-[3px] border-[#102f5b] bg-brand px-3 py-2 font-display text-sm uppercase text-white shadow-[0_3px_0_#102f5b] transition-colors hover:bg-brand-strong" to={ROUTES.play}>
                  Começar uma run
                </Link>
              </>
            ) : (
              <>
                <p className="mb-0 mt-3 text-base leading-snug text-[#102f5b]">Entre para registrar suas vitórias no ranking.</p>
                <Link className="mt-4 inline-flex min-h-12 w-full items-center justify-center border-[3px] border-[#102f5b] bg-brand px-3 py-2 font-display text-sm uppercase text-white shadow-[0_3px_0_#102f5b] transition-colors hover:bg-brand-strong" to={ROUTES.login}>
                  Entrar / criar conta
                </Link>
              </>
            )}
          </div>
        </aside>
      </div>

    </div>
  )
}
