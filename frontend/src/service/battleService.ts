import type { AuthSession } from '../types/account'
import type { BattleTurn, BattleView } from '../types/battle'
import type { RunSession } from '../types/run'
import apiRequest, { ApiError } from './apiClient'
import { getRunHeaders } from './runService'

let activeStartRequest: { runId: string; promise: Promise<BattleTurn> } | null = null

export function getCurrentBattle(run: RunSession, session: AuthSession | null): Promise<BattleView> {
  return apiRequest<BattleView>(`/runs/${run.runId}/battles/current`, {
    headers: getRunHeaders(run, session),
  })
}

async function requestBattleTurn(run: RunSession, session: AuthSession | null): Promise<BattleTurn> {
  return apiRequest<BattleTurn>(`/runs/${run.runId}/battles/current/start`, {
    method: 'POST',
    headers: getRunHeaders(run, session),
  })
}

async function waitForBattleCompletion(run: RunSession, session: AuthSession | null): Promise<BattleTurn> {
  const deadline = Date.now() + 60_000
  let result = await requestBattleTurn(run, session)
  const events = [...result.events]

  while (result.status === 'RUNNING' && Date.now() < deadline) {
    await new Promise((resolve) => window.setTimeout(resolve, 400))
    result = await requestBattleTurn(run, session)
    events.push(...result.events)
  }

  if (result.status === 'RUNNING') {
    throw new ApiError('A batalha ainda está sendo simulada. Tente novamente em instantes.', 503)
  }

  return { ...result, events }
}

export function startCurrentBattle(run: RunSession, session: AuthSession | null): Promise<BattleTurn> {
  if (activeStartRequest?.runId === run.runId) return activeStartRequest.promise

  const request = waitForBattleCompletion(run, session).finally(() => {
    if (activeStartRequest?.promise === request) activeStartRequest = null
  })

  activeStartRequest = { runId: run.runId, promise: request }
  return request
}

export function submitBattleChoice(
  run: RunSession,
  session: AuthSession | null,
  battleNumber: number,
  choice: string,
): Promise<BattleTurn> {
  return apiRequest<BattleTurn>(`/runs/${run.runId}/battles/${battleNumber}/choices`, {
    method: 'POST',
    headers: getRunHeaders(run, session),
    body: JSON.stringify({ choice }),
  })
}
