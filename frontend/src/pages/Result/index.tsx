import { useEffect, useState } from 'react'
import { FaRotateRight, FaTrophy } from 'react-icons/fa6'
import { TbPokeball } from 'react-icons/tb'
import { Link, useLocation, useNavigate, useParams } from 'react-router'
import PokemonSprite from '../../components/PokemonSprite/PokemonSprite'
import useAuth from '../../components/AuthProvider/useAuth'
import { ApiError } from '../../service/apiClient'
import {
  challengePreviousChampion,
  getRunOutcome,
  getRunSession,
  getRunTeam,
  publishCompletedRunToRanking,
  storeClaimedRunSession,
} from '../../service/runService'
import { ROUTES } from '../../routes/paths'
import type { ChampionChallenge, RunOutcome, RunSession, RunTeamMember } from '../../types/run'

const confettiPositions = [
  'left-[5%] top-[18%]', 'left-[19%] top-[8%]', 'left-[31%] top-[29%]',
  'left-[49%] top-[13%]', 'left-[64%] top-[25%]', 'left-[81%] top-[9%]',
  'left-[93%] top-[34%]', 'left-[11%] top-[58%]', 'left-[39%] top-[52%]',
  'left-[71%] top-[55%]', 'left-[88%] top-[63%]',
]

const confettiColors = ['bg-red-500', 'bg-yellow-300', 'bg-sky-300', 'bg-white']

const previewTeam: RunTeamMember[] = [
  { slot_number: 1, pokemon_id: 'preview-charizard', pokemon_name: 'Charizard', primary_type: 'fire', secondary_type: 'flying', front_sprite_url: null, back_sprite_url: null, national_dex_number: 6, build_snapshot: {} },
  { slot_number: 2, pokemon_id: 'preview-dragonite', pokemon_name: 'Dragonite', primary_type: 'dragon', secondary_type: 'flying', front_sprite_url: null, back_sprite_url: null, national_dex_number: 149, build_snapshot: {} },
  { slot_number: 3, pokemon_id: 'preview-alakazam', pokemon_name: 'Alakazam', primary_type: 'psychic', secondary_type: null, front_sprite_url: null, back_sprite_url: null, national_dex_number: 65, build_snapshot: {} },
  { slot_number: 4, pokemon_id: 'preview-gengar', pokemon_name: 'Gengar', primary_type: 'ghost', secondary_type: 'poison', front_sprite_url: null, back_sprite_url: null, national_dex_number: 94, build_snapshot: {} },
  { slot_number: 5, pokemon_id: 'preview-gyarados', pokemon_name: 'Gyarados', primary_type: 'water', secondary_type: 'flying', front_sprite_url: null, back_sprite_url: null, national_dex_number: 130, build_snapshot: {} },
  { slot_number: 6, pokemon_id: 'preview-vaporeon', pokemon_name: 'Vaporeon', primary_type: 'water', secondary_type: null, front_sprite_url: null, back_sprite_url: null, national_dex_number: 134, build_snapshot: {} },
]

function formatDate(value: string | null): string {
  if (!value) return 'Agora mesmo'
  return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'long' }).format(new Date(value))
}

function actionClass(primary = false) {
  return `inline-flex min-h-12 items-center justify-center gap-2 border-[3px] border-[#14233d] px-5 py-2 font-display text-sm uppercase shadow-[0_3px_0_#14233d] transition-colors sm:px-7 sm:text-base ${
    primary
      ? 'bg-brand text-white hover:bg-brand-strong'
      : 'bg-paper text-[#14233d] hover:bg-[#e9e3d8]'
  }`
}

export default function ResultPage() {
  const { runId } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const { session } = useAuth()
  const isPreview = import.meta.env.DEV && new URLSearchParams(location.search).get('preview') === 'champion'
  const [run, setRun] = useState<RunSession | null>(() => getRunSession())
  const [outcome, setOutcome] = useState<RunOutcome | null>(null)
  const [team, setTeam] = useState<RunTeamMember[]>([])
  const [challenge, setChallenge] = useState<ChampionChallenge | null>(null)
  const [challenging, setChallenging] = useState(false)
  const [challengeError, setChallengeError] = useState<string | null>(null)
  const [publishing, setPublishing] = useState(false)
  const [published, setPublished] = useState(false)
  const [publishError, setPublishError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (isPreview) {
      const previewRunId = runId ?? 'champion-preview'
      setRun((currentRun) => currentRun ?? { runId: previewRunId, ownerType: 'guest', guestSessionToken: null })
      setOutcome({
        run: { id: previewRunId, status: 'COMPLETED', stage: 'RESULT', progress_index: 13, reroll_used: false, legendary_selected: false, created_at: new Date().toISOString(), ended_at: new Date().toISOString() },
        hall_of_fame_snapshot: null,
        champion_history: null,
      })
      setTeam(previewTeam)
      setLoading(false)
      return
    }

    if (!run || !runId || run.runId !== runId) {
      setError('Não encontramos a equipe desta run neste navegador.')
      setLoading(false)
      return
    }

    let cancelled = false
    Promise.all([getRunOutcome(run, session), getRunTeam(run, session)])
      .then(([runOutcome, runTeam]) => {
        if (cancelled) return
        if (runOutcome.run.status !== 'COMPLETED') {
          setError('Esta run ainda não foi concluída como campeã.')
          return
        }
        setOutcome(runOutcome)
        setTeam(runTeam)
      })
      .catch(() => {
        if (!cancelled) setError('Não foi possível carregar o resultado da sua run.')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => { cancelled = true }
  }, [isPreview, run, runId, session])

  async function handleChampionChallenge() {
    if (!run || challenging) return
    setChallenging(true)
    setChallengeError(null)
    setChallenge(null)
    try {
      setChallenge(await challengePreviousChampion(run, session))
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 404) {
        setChallengeError('Ainda não há um time campeão anterior salvo para desafiar.')
      } else if (reason instanceof ApiError && reason.status === 503) {
        setChallengeError('O motor de batalha está indisponível. Tente novamente em instantes.')
      } else {
        setChallengeError('Não foi possível simular a revanche. Tente novamente.')
      }
    } finally {
      setChallenging(false)
    }
  }

  async function handlePublish() {
    if (!run || !session || publishing) return
    setPublishing(true)
    setPublishError(null)
    try {
      await publishCompletedRunToRanking(run, session)
      setRun(storeClaimedRunSession(run))
      setPublished(true)
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 401) {
        setPublishError('Entre novamente na sua conta para publicar esta vitória.')
      } else {
        setPublishError('Não foi possível publicar a vitória no ranking. Tente novamente.')
      }
    } finally {
      setPublishing(false)
    }
  }

  if (loading) {
    return <p aria-live="polite" className="m-0 px-4 py-24 text-center font-display uppercase text-graphite-muted">Preparando sua conquista…</p>
  }

  if (error || !outcome || !run) {
    return (
      <section className="mx-auto max-w-2xl px-4 py-16 text-center">
        <h1 className="m-0 font-display text-2xl uppercase text-graphite">Resultado indisponível</h1>
        <p className="mb-0 mt-3 text-graphite-muted">{error ?? 'Não foi possível encontrar os dados desta run.'}</p>
        <button className="mt-6 border-2 border-graphite bg-surface px-5 py-2 font-display uppercase hover:border-brand-strong" onClick={() => navigate(ROUTES.home)} type="button">
          Voltar ao início
        </button>
      </section>
    )
  }

  const needsRankingClaim = (isPreview || run.ownerType === 'guest') && !published
  const loginReturnPath = `${location.pathname}${location.search}`

  return (
    <div className="pb-8">
      <section aria-label="Vitória do campeão" className="mt-4 overflow-hidden bg-[#1a2d50] sm:mt-6">
        <div className="border-b-[3px] border-[#122039] bg-[#182a49] px-3 py-3 text-white shadow-[inset_0_-5px_0_rgb(255_255_255_/_5%)] sm:px-8 sm:py-4">
          <div className="mx-auto flex max-w-[100rem] flex-col items-center gap-2 sm:flex-row sm:gap-8">
            <h2 className="m-0 shrink-0 font-display text-base uppercase tracking-wider sm:text-2xl">13 / 13 vitórias</h2>
            <ol aria-label="13 de 13 batalhas vencidas" className="relative m-0 flex w-full list-none items-center justify-between p-0 before:absolute before:left-2 before:right-2 before:top-1/2 before:h-1 before:-translate-y-1/2 before:bg-brand sm:before:left-4 sm:before:right-4">
              {Array.from({ length: 13 }, (_, index) => (
                <li key={index} className="relative z-10 grid size-7 shrink-0 place-items-center rounded-full bg-[#182a49] text-brand sm:size-9">
                  <TbPokeball aria-hidden="true" className="text-xl sm:text-2xl" />
                </li>
              ))}
            </ol>
          </div>
        </div>

        <div
          className="relative mx-auto min-h-[520px] max-w-[110rem] overflow-hidden bg-[#31599a] sm:min-h-[650px]"
          style={{ backgroundImage: 'repeating-linear-gradient(0deg, #31599a 0, #31599a 9px, #294f89 9px, #294f89 18px)' }}
        >
          <div aria-hidden="true" className="pointer-events-none absolute inset-0">
            {confettiPositions.map((position, index) => (
              <span key={position} className={`absolute ${position} size-2.5 sm:size-3 ${confettiColors[index % confettiColors.length]}`} />
            ))}
          </div>

          <ul aria-label="Pokémon do time campeão" className="absolute inset-x-0 top-4 bottom-28 mx-auto m-0 grid w-full max-w-[56rem] list-none grid-cols-3 grid-rows-2 items-center justify-items-center gap-x-0 gap-y-0 p-0 sm:top-6 sm:bottom-32">
            {team.map((member) => (
              <li
                key={`${member.pokemon_id}-${member.slot_number}`}
                className="flex min-w-0 items-center justify-center drop-shadow-[0_5px_0_rgb(13_30_59_/_35%)]"
              >
                <PokemonSprite
                  name={member.pokemon_name}
                  pokedexNumber={member.national_dex_number ?? undefined}
                  spriteUrl={member.front_sprite_url}
                  size="celebration"
                />
              </li>
            ))}
          </ul>

          <div className="absolute bottom-5 left-4 right-4 z-20 border-[4px] border-[#14233d] bg-paper px-3 py-4 text-center shadow-[5px_5px_0_rgb(13_30_59_/_50%)] sm:bottom-7 sm:left-[9%] sm:right-[9%] sm:px-8 sm:py-5">
            <h1 className="m-0 font-display text-2xl uppercase leading-tight text-[#14233d] sm:text-4xl lg:text-5xl">Você é o campeão!</h1>
            <p className="mb-0 mt-1 font-display text-sm uppercase leading-tight text-[#14233d] sm:mt-2 sm:text-xl lg:text-2xl">Sua jornada chegou ao fim</p>
          </div>
        </div>
      </section>

      <section className="mx-auto flex max-w-5xl flex-col items-center px-4 py-5 text-center sm:py-7">
        <div className="flex flex-wrap justify-center gap-3">
          {needsRankingClaim && (!session || isPreview) && (
            <Link className={actionClass(true)} state={{ returnTo: loginReturnPath }} to={ROUTES.login}>
              Entrar e publicar no ranking
            </Link>
          )}
          {needsRankingClaim && session && isPreview && (
            <button aria-disabled="true" className={`${actionClass(true)} cursor-not-allowed opacity-80`} type="button">
              Entrar e publicar no ranking
            </button>
          )}
          {needsRankingClaim && session && !isPreview && (
            <button className={actionClass(true)} disabled={publishing} onClick={handlePublish} type="button">
              {publishing ? 'Publicando…' : 'Publicar no ranking'}
            </button>
          )}
          {!needsRankingClaim && !isPreview && (
            <span className="inline-flex min-h-12 items-center gap-2 border-[3px] border-[#14233d] bg-[#e6eee3] px-5 py-2 font-display text-sm uppercase text-[#14233d] sm:text-base">
              <FaTrophy aria-hidden="true" className="text-[#bd8b28]" />
              {published ? 'Vitória publicada no ranking' : 'Vitória registrada no ranking'}
            </span>
          )}
          <button className={actionClass()} onClick={() => navigate(ROUTES.play)} type="button">
            <FaRotateRight aria-hidden="true" />
            Jogar novamente
          </button>
          <button className={actionClass()} onClick={() => navigate(ROUTES.home)} type="button">
            Voltar ao início
          </button>
        </div>

        {needsRankingClaim && !session && <p className="mb-0 mt-2 text-sm text-[#536987]">A vitória será publicada após entrar na conta.</p>}
        {publishError && <p aria-live="polite" className="mb-0 mt-3 border-2 border-danger bg-surface px-3 py-2 text-sm text-danger">{publishError}</p>}

        {!isPreview && (
          <>
            <button className="mt-4 min-h-10 border-b-2 border-[#14233d] px-2 font-display text-sm uppercase text-[#14233d] hover:border-brand hover:text-brand-strong" disabled={challenging} onClick={handleChampionChallenge} type="button">
              {challenging ? 'Simulando revanche…' : 'Enfrentar o último campeão'}
            </button>
            {challengeError && <p aria-live="polite" className="mb-0 mt-3 border-2 border-danger bg-surface px-3 py-2 text-sm text-danger">{challengeError}</p>}
          </>
        )}
      </section>

      {!isPreview && challenge && (
        <section aria-labelledby="challenge-result-heading" className="mx-auto mt-2 w-full max-w-5xl px-4">
          <div className="border-[3px] border-[#14233d] bg-surface p-4 shadow-pixel sm:p-6">
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <h2 id="challenge-result-heading" className="m-0 font-display text-lg uppercase text-graphite sm:text-xl">
                {challenge.simulator_result === 'WIN' ? 'Revanche vencida!' : challenge.simulator_result === 'LOSS' ? 'O último campeão venceu' : 'A revanche terminou empatada'}
              </h2>
              <span className="text-sm text-graphite-muted">{challenge.champion_name} · campeão em {formatDate(challenge.became_champion_at)}</span>
            </div>
            <ul aria-label={`Time de ${challenge.champion_name}`} className="m-0 mt-4 grid list-none grid-cols-3 gap-2 p-0 sm:grid-cols-6 sm:gap-3">
              {challenge.team.map((member, index) => (
                <li key={`${member.pokemon_id}-${index}`} className="flex min-h-28 flex-col items-center justify-center border-2 border-border bg-paper px-1 py-2 text-center">
                  <PokemonSprite name={member.pokemon_name} pokedexNumber={member.national_dex_number ?? undefined} spriteUrl={member.front_sprite_url} size="compact" />
                  <span className="mt-1 font-display text-xs uppercase leading-tight text-graphite">{member.pokemon_name}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>
      )}
    </div>
  )
}
