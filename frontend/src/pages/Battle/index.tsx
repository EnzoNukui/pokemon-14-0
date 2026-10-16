import { useCallback, useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import BattleArena from '../../components/BattleArena/BattleArena'
import BattleDialog from '../../components/BattleDialog/BattleDialog'
import BattleProgress from '../../components/BattleProgress/BattleProgress'
import type { BattleSpeed } from '../../components/BattleSpeedControl/BattleSpeedControl'
import { ApiError } from '../../service/apiClient'
import { getCurrentBattle, startCurrentBattle } from '../../service/battleService'
import { getRunSession, getRunTeam } from '../../service/runService'
import { ROUTES } from '../../routes/paths'
import type { BattleEvent, BattleTurn, BattleView } from '../../types/battle'
import type { RunSession, RunTeamMember } from '../../types/run'
import useAuth from '../../components/AuthProvider/useAuth'

type BattleLogEntry = {
  event: BattleEvent
  message: string
}

function formatApiError(error: unknown): string {
  if (error instanceof ApiError) {
    if (error.status === 0) return error.message
    if (error.status === 401) return 'A sessão desta run expirou. Volte ao jogo para iniciar outra.'
    if (error.status === 503) return error.message
    return error.message
  }
  return 'Não foi possível carregar a batalha. Tente novamente.'
}

function eventMessage(event: BattleEvent): string | null {
  const parts = Array.isArray(event.payload.parts)
    ? event.payload.parts.filter((part): part is string => typeof part === 'string')
    : []
  const name = (value?: string) => value?.replace(/^p[12][a-z]:\s*/i, '').trim() || 'Pokémon'
  const move = (value?: string) => value?.replace(/-/g, ' ').replace(/\b\w/g, (letter) => letter.toLocaleUpperCase()) || 'um movimento'

  switch (event.event_type) {
    case 'start': return 'A batalha começou!'
    case 'turn': return `Turno ${parts[0] ?? ''}`.trim()
    case 'switch':
    case 'drag': return `${name(parts[0])} entrou em campo!`
    case 'move': return `${name(parts[0])} usou ${move(parts[1])}!`
    case '-damage':
    case '-heal':
    case '-sethp': return null
    case 'faint': return `${name(parts[0])} foi derrotado.`
    case '-supereffective': return 'Foi super eficaz!'
    case '-resisted': return 'Não foi muito eficaz…'
    case '-miss': return `${name(parts[0])} errou o ataque.`
    case '-status': return `${name(parts[0])} sofreu uma alteração de estado.`
    case 'cant': return `${name(parts[0])} não conseguiu agir.`
    case 'win': return parts[0] === 'Player' ? 'Seu time venceu esta batalha!' : `${parts[0] ?? 'O adversário'} venceu a batalha.`
    case 'tie': return 'Empate! O desafio termina sem uma vitória.'
    default: return null
  }
}

function entriesFrom(events: BattleEvent[]): BattleLogEntry[] {
  return events.flatMap((event) => {
    const message = eventMessage(event)
    const updatesScene = ['-damage', '-heal', '-sethp'].includes(event.event_type)
    return message || updatesScene ? [{ event, message: message ?? '' }] : []
  })
}

export default function BattlePage() {
  const { session: authSession } = useAuth()
  const navigate = useNavigate()
  const [run] = useState<RunSession | null>(() => getRunSession())
  const [team, setTeam] = useState<RunTeamMember[]>([])
  const [battle, setBattle] = useState<BattleView | null>(null)
  const [turn, setTurn] = useState<BattleTurn | null>(null)
  const [logEntries, setLogEntries] = useState<BattleLogEntry[]>([])
  const [shownMessageCount, setShownMessageCount] = useState(0)
  const [speed, setSpeed] = useState<BattleSpeed>('slow')
  const [paused, setPaused] = useState(false)
  const [busy, setBusy] = useState<'load' | 'next' | null>('load')
  const [error, setError] = useState<string | null>(null)

  const loadCurrentBattle = useCallback(async (activeRun: RunSession) => {
    const [currentTeam, currentBattle] = await Promise.all([
      getRunTeam(activeRun, authSession),
      getCurrentBattle(activeRun, authSession),
    ])
    if (currentTeam.length !== 6) {
      navigate(ROUTES.draft, { replace: true })
      return
    }

    setTeam(currentTeam)
    setBattle(currentBattle)
    setTurn(null)
    setLogEntries([])
    setShownMessageCount(0)
    setPaused(false)
    setError(null)

    if (currentBattle.status === 'PENDING' || currentBattle.status === 'RUNNING') {
      const result = await startCurrentBattle(activeRun, authSession)
      setTurn(result)
      setLogEntries(entriesFrom(result.events))
    }
  }, [authSession, navigate])

  useEffect(() => {
    if (!run) {
      navigate(ROUTES.play, { replace: true })
      return
    }
    let cancelled = false

    void loadCurrentBattle(run).catch((reason: unknown) => {
      if (!cancelled) {
        if (reason instanceof ApiError && reason.status === 409) {
          navigate(ROUTES.draft, { replace: true })
          return
        }
        setError(formatApiError(reason))
      }
    }).finally(() => {
      if (!cancelled) setBusy(null)
    })

    return () => { cancelled = true }
  }, [loadCurrentBattle, navigate, run])

  useEffect(() => {
    if (paused || shownMessageCount >= logEntries.length) return
    const delay = speed === 'slow' ? 420 : speed === 'normal' ? 180 : 70
    const timer = window.setTimeout(() => setShownMessageCount((count) => count + 1), delay)
    return () => window.clearTimeout(timer)
  }, [logEntries.length, paused, shownMessageCount, speed])

  async function handleNextBattle() {
    if (!run || busy) return
    setBusy('next')
    setError(null)
    try {
      await loadCurrentBattle(run)
    } catch (reason) {
      setError(formatApiError(reason))
    } finally {
      setBusy(null)
    }
  }

  const isBattleComplete = turn?.status === 'COMPLETED' || battle?.status === 'COMPLETED'
  const canContinue = isBattleComplete && turn?.run_status === 'ACTIVE' && turn.next_battle_number !== null
  const visibleEntries = logEntries.slice(0, shownMessageCount)
  const visibleMessages = visibleEntries.map((entry) => entry.message).filter(Boolean)
  const visibleEvents = visibleEntries.map((entry) => entry.event)
  const finalMessageIndex = logEntries.reduce(
    (lastIndex, entry, index) => entry.message ? index : lastIndex,
    -1,
  )
  const replayFinished = shownMessageCount > finalMessageIndex

  return (
    <section className="mx-auto w-full max-w-[100rem] px-3 pb-8 sm:px-7">
      {battle && <BattleProgress battleNumber={turn?.battle_number ?? battle.battle_number} />}

      {error && <p aria-live="assertive" className="mx-auto mb-4 mt-4 max-w-3xl border-2 border-danger bg-surface px-4 py-3 text-center text-sm text-danger">{error}</p>}

      {isBattleComplete && replayFinished && (
        <section aria-live="polite" className="mx-auto mt-4 w-full max-w-6xl border-[3px] border-graphite bg-paper p-4 text-center shadow-[3px_3px_0_rgb(53_53_58_/_14%)] sm:p-5">
          <h2 className="m-0 font-display text-xl uppercase text-brand-strong sm:text-2xl">
            {turn?.simulator_result === 'DRAW' ? 'Empate' : turn?.run_status === 'COMPLETED' ? 'Campeão!' : canContinue ? 'Batalha vencida!' : turn?.run_status === 'FAILED' ? 'Fim da run' : 'Batalha encerrada'}
          </h2>
          <p className="mb-0 mt-1 text-sm text-graphite-muted">
            {turn?.simulator_result === 'DRAW' ? 'O empate encerra a run e não conta como vitória.' : canContinue ? `Próximo desafio: batalha ${turn?.next_battle_number} de 13.` : turn?.run_status === 'COMPLETED' ? 'Você venceu os 13 treinadores e concluiu o desafio.' : turn?.run_status === 'FAILED' ? 'Sua sequência de vitórias terminou nesta batalha.' : 'O resultado foi registrado.'}
          </p>
          {canContinue ? (
            <button className="mt-3 min-h-11 border-[3px] border-graphite bg-brand px-6 font-display uppercase text-white shadow-[2px_2px_0_#35353a] hover:bg-brand-strong disabled:opacity-50" disabled={busy !== null} onClick={handleNextBattle} type="button">
              {busy === 'next' ? 'Preparando…' : 'Próximo treinador'}
            </button>
          ) : (
            <button className="mt-3 min-h-11 border-2 border-graphite bg-surface px-6 font-display uppercase text-graphite hover:border-brand-strong" onClick={() => navigate(ROUTES.play)} type="button">Jogar novamente</button>
          )}
        </section>
      )}

      {busy === 'load' && !battle ? (
        <p aria-live="polite" className="m-0 py-16 text-center font-display uppercase text-graphite-muted">Preparando o desafio…</p>
      ) : battle ? (
        <div className="mx-auto mt-4 grid max-w-6xl gap-3 sm:mt-5 sm:gap-4">
          {(busy === 'load' || busy === 'next') && (
            <p aria-live="polite" className="m-0 border-2 border-brand-strong bg-paper px-4 py-2 text-center font-display text-sm uppercase text-graphite">
              Simulando a batalha…
            </p>
          )}
          <BattleArena
            key={battle.id}
            battleNumber={turn?.battle_number ?? battle.battle_number}
            trainerName={battle.trainer_name}
            trainerSpriteUrl={battle.trainer_sprite_url}
            playerTeam={team}
            opponentTeam={battle.opponent_team}
            events={visibleEvents}
          />

          <BattleDialog messages={visibleMessages} speed={speed} paused={paused} onSpeedChange={setSpeed} onPauseToggle={() => setPaused((current) => !current)} />
        </div>
      ) : (
        <div className="mx-auto max-w-xl py-10 text-center">
          <p className="text-graphite-muted">{error ?? 'Não há uma batalha disponível para esta run.'}</p>
          <button className="mt-3 border-2 border-graphite bg-surface px-5 py-2 font-display uppercase hover:border-brand-strong" onClick={() => navigate(ROUTES.draft)} type="button">Voltar ao time</button>
        </div>
      )}
    </section>
  )
}
