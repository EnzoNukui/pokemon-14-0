import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import DraftControls from '../../components/DraftControls/DraftControls'
import DraftSlots from '../../components/DraftSlots/DraftSlots'
import PokemonSprite from '../../components/PokemonSprite/PokemonSprite'
import { ApiError } from '../../service/apiClient'
import {
  abandonRun,
  clearRunSession,
  getDraftRound,
  getRunSession,
  getRunTeam,
  rerollDraftRound,
  selectDraftOption,
} from '../../service/runService'
import { ROUTES } from '../../routes/paths'
import type { DraftOption, DraftRound, RunSession, RunTeamMember } from '../../types/run'
import useAuth from '../../components/AuthProvider/useAuth'

function formatError(error: unknown): string {
  if (error instanceof ApiError) {
    if (error.status === 0) return error.message
    if (error.status === 401) return 'A sessão desta run expirou. Inicie uma nova run.'
    if (error.status === 503) return error.message
    return error.message
  }
  return 'Não foi possível carregar esta rodada. Tente novamente.'
}

function FrameCorner({ position }: { position: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' }) {
  const placement = {
    'top-left': 'left-1 top-1 border-l-[3px] border-t-[3px]',
    'top-right': 'right-1 top-1 border-r-[3px] border-t-[3px]',
    'bottom-left': 'bottom-1 left-1 border-b-[3px] border-l-[3px]',
    'bottom-right': 'bottom-1 right-1 border-b-[3px] border-r-[3px]',
  }[position]

  return (
    <span
      aria-hidden="true"
      className={`pointer-events-none absolute z-10 size-5 border-brand-strong sm:size-7 ${placement}`}
    />
  )
}

export default function DraftPage() {
  const { session: authSession } = useAuth()
  const navigate = useNavigate()
  const [run, setRun] = useState<RunSession | null>(null)
  const [round, setRound] = useState<DraftRound | null>(null)
  const [team, setTeam] = useState<RunTeamMember[]>([])
  const [selectedOptionNumber, setSelectedOptionNumber] = useState<number | null>(null)
  const [busyAction, setBusyAction] = useState<'load' | 'select' | 'reroll' | 'restart' | null>('load')
  const [complete, setComplete] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const savedRun = getRunSession()
    if (!savedRun) {
      navigate(ROUTES.play, { replace: true })
      return
    }
    setRun(savedRun)
  }, [navigate])

  useEffect(() => {
    if (!run) return
    let cancelled = false
    setBusyAction('load')
    setError(null)

    void Promise.allSettled([
      getRunTeam(run, authSession),
      getDraftRound(run, authSession),
    ]).then(([teamResult, roundResult]) => {
      if (cancelled) return
      if (teamResult.status === 'rejected') {
        setError(formatError(teamResult.reason))
        return
      }

      setTeam(teamResult.value)
      if (roundResult.status === 'fulfilled') {
        setRound(roundResult.value)
        setComplete(false)
      } else if (roundResult.reason instanceof ApiError && roundResult.reason.status === 409 && teamResult.value.length === 6) {
        setRound(null)
        setComplete(true)
      } else {
        setError(formatError(roundResult.reason))
      }
    }).finally(() => {
      if (!cancelled) setBusyAction(null)
    })

    return () => {
      cancelled = true
    }
  }, [authSession, run])

  const selectedOption: DraftOption | null =
    round?.options.find((option) => option.option_number === selectedOptionNumber) ?? null

  function handleChooseOption(option: DraftOption, rareBlocked: boolean) {
    if (isBusy) return
    if (rareBlocked) {
      setSelectedOptionNumber(null)
      setError('Não é possível ter mais de um lendário ou mítico no time.')
      return
    }
    setError(null)
    setSelectedOptionNumber(option.option_number)
  }

  async function handleSelect() {
    if (!run || !selectedOption || busyAction) return
    setBusyAction('select')
    setError(null)

    try {
      const selection = await selectDraftOption(run, authSession, selectedOption)
      const nextTeamPromise = getRunTeam(run, authSession)
      if (selection.draft_complete) {
        setTeam(await nextTeamPromise)
        setRound(null)
        setComplete(true)
      } else {
        const [nextTeam, nextRound] = await Promise.all([
          nextTeamPromise,
          getDraftRound(run, authSession),
        ])
        setTeam(nextTeam)
        setRound(nextRound)
        setComplete(false)
      }
      setSelectedOptionNumber(null)
    } catch (reason) {
      setError(formatError(reason))
    } finally {
      setBusyAction(null)
    }
  }

  async function handleReroll() {
    if (!run || !round?.reroll_available || busyAction) return
    setBusyAction('reroll')
    setError(null)

    try {
      const nextRound = await rerollDraftRound(run, authSession)
      setRound(nextRound)
      setSelectedOptionNumber(null)
    } catch (reason) {
      setError(formatError(reason))
    } finally {
      setBusyAction(null)
    }
  }

  async function handleRestart() {
    if (!run || busyAction) return
    setBusyAction('restart')
    setError(null)
    try {
      await abandonRun(run, authSession)
      clearRunSession()
      navigate(ROUTES.play, { replace: true })
    } catch (reason) {
      setError(formatError(reason))
      setBusyAction(null)
    }
  }

  const roundNumber = complete ? 6 : round?.round_number ?? team.length + 1
  const isBusy = busyAction !== null

  return (
    <section className="mx-auto w-full max-w-[90rem] px-3 py-6 sm:px-8 sm:py-9">
      <div className="relative border-[3px] border-brand-strong bg-paper px-4 py-6 shadow-[inset_0_0_0_2px_#35353a] sm:px-8 sm:py-8 md:px-12 md:py-9">
        <FrameCorner position="top-left" />
        <FrameCorner position="top-right" />
        <FrameCorner position="bottom-left" />
        <FrameCorner position="bottom-right" />

        <header className="mx-auto flex max-w-3xl flex-col items-center">
          <div className="flex w-full items-center gap-2 text-brand-strong sm:gap-3">
            <span aria-hidden="true" className="h-[3px] flex-1 bg-brand-strong" />
            <span aria-hidden="true" className="size-2 rotate-45 border-2 border-brand-strong bg-paper" />
            <h1 className="m-0 border-[3px] border-brand-strong bg-surface px-4 py-1.5 text-center font-display text-xl uppercase text-graphite sm:px-8 sm:text-3xl">
              Escolha seu time
            </h1>
            <span aria-hidden="true" className="size-2 rotate-45 border-2 border-brand-strong bg-paper" />
            <span aria-hidden="true" className="h-[3px] flex-1 bg-brand-strong" />
          </div>

          <div className="mt-1 flex items-center gap-3 text-brand-strong sm:gap-5">
            <span aria-hidden="true" className="h-[3px] w-8 bg-brand-strong sm:w-16" />
            <span className="border-[3px] border-brand-strong bg-surface px-5 py-0.5 font-display text-base text-graphite sm:px-8 sm:text-xl">
              {roundNumber} / 6
            </span>
            <span aria-hidden="true" className="h-[3px] w-8 bg-brand-strong sm:w-16" />
          </div>
        </header>

        <div className="mx-auto mt-5 max-w-4xl sm:mt-6">
          <DraftSlots team={team} />
        </div>

        <div className="my-6 flex items-center gap-2 sm:my-7 sm:gap-4">
          <span aria-hidden="true" className="h-[3px] flex-1 bg-brand-strong" />
          <span aria-hidden="true" className="size-3 rotate-45 border-[3px] border-brand-strong bg-paper" />
          <h2 className="m-0 border-[3px] border-brand-strong bg-surface px-4 py-1 font-display text-base uppercase text-graphite sm:px-7 sm:text-xl">
            {complete ? 'Time completo' : 'Opções da rodada'}
          </h2>
          <span aria-hidden="true" className="size-3 rotate-45 border-[3px] border-brand-strong bg-paper" />
          <span aria-hidden="true" className="h-[3px] flex-1 bg-brand-strong" />
        </div>

        {error && (
          <p aria-live="polite" className="mx-auto my-5 max-w-xl border-2 border-danger bg-surface px-4 py-3 text-center text-sm text-danger">
            {error}
          </p>
        )}

        {!complete && round && (
          <ul className="mx-auto m-0 grid max-w-[52rem] list-none grid-cols-2 gap-3 p-0 sm:grid-cols-3 sm:gap-4 md:gap-5">
            {round.options.map((option) => {
              const selected = option.option_number === selectedOptionNumber
              const rareOption = option.is_legendary || option.is_mythical
              const rareBlocked = rareOption && round.legendary_selected
              return (
                <li key={option.pokemon_id}>
                  <button
                    aria-pressed={selected}
                    aria-disabled={rareBlocked}
                    title={rareBlocked ? 'O único lendário ou mítico desta run já foi escolhido.' : undefined}
                    className={`group relative flex min-h-40 w-full flex-col items-center justify-between overflow-hidden border-[3px] bg-surface p-2 shadow-[inset_0_0_0_2px_#35353a,2px_2px_0_rgb(53_53_58_/_18%)] transition sm:min-h-44 sm:p-3 ${rareBlocked ? 'cursor-pointer border-graphite/35 opacity-55 grayscale hover:opacity-80' : selected ? 'border-brand bg-brand-soft' : 'border-graphite/75 hover:border-brand-strong hover:bg-brand-soft/50'}`}
                    disabled={isBusy}
                    onClick={() => handleChooseOption(option, rareBlocked)}
                    type="button"
                  >
                    <span aria-hidden="true" className="absolute left-1 top-1 size-2 border-l-2 border-t-2 border-brand-strong" />
                    <span aria-hidden="true" className="absolute right-1 top-1 size-2 border-r-2 border-t-2 border-brand-strong" />
                    <span aria-hidden="true" className="absolute bottom-1 left-1 size-2 border-b-2 border-l-2 border-brand-strong" />
                    <span aria-hidden="true" className="absolute bottom-1 right-1 size-2 border-b-2 border-r-2 border-brand-strong" />
                    <span className="grid min-h-28 flex-1 place-items-center sm:min-h-32">
                      <PokemonSprite
                        name={option.name}
                        pokedexNumber={option.national_dex_number ?? undefined}
                        spriteUrl={option.front_sprite_url}
                      />
                    </span>
                    <span className="w-full border-t-2 border-graphite/65 bg-surface-muted px-2 py-1 font-display text-sm uppercase leading-none text-graphite sm:text-base">
                      {option.name}
                    </span>
                  </button>
                </li>
              )
            })}
          </ul>
        )}

        {busyAction === 'load' && !round && !complete && (
          <p aria-live="polite" className="m-0 py-10 text-center font-display text-base uppercase text-graphite-muted">
            Preparando a rodada…
          </p>
        )}

        {complete && (
          <div className="flex flex-col items-center gap-4 py-7 text-center">
            <p aria-live="polite" className="m-0 font-display text-base uppercase text-graphite-muted">
              Seu time está pronto.
            </p>
            <button
              className="min-h-12 border-[3px] border-graphite bg-brand px-7 font-display text-lg uppercase text-white shadow-[3px_3px_0_#35353a] hover:bg-brand-strong"
              onClick={() => navigate(ROUTES.battle)}
              type="button"
            >
              Iniciar desafio
            </button>
          </div>
        )}

        {!complete && round && (
          <DraftControls
            busyAction={busyAction === 'select' || busyAction === 'reroll' ? busyAction : null}
            canReroll={round.reroll_available}
            canSelect={selectedOption !== null}
            onReroll={handleReroll}
            onSelect={handleSelect}
          />
        )}

        {run && (
          <div className="mt-5 flex justify-center">
            <button
              className="min-h-10 border-2 border-graphite/70 bg-surface px-4 py-2 font-display text-xs uppercase text-graphite-muted transition hover:border-brand-strong hover:text-brand-strong disabled:cursor-not-allowed disabled:opacity-50 sm:text-sm"
              disabled={isBusy}
              onClick={handleRestart}
              type="button"
            >
              {busyAction === 'restart' ? 'Recomeçando…' : 'Sair deste time e começar do zero'}
            </button>
          </div>
        )}
      </div>
    </section>
  )
}
