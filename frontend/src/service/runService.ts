import type { AuthSession } from '../types/account'
import type {
  ChampionChallenge,
  DraftOption,
  DraftRound,
  DraftSelection,
  RunOutcome,
  RunResponse,
  RunSession,
  RunTeamMember,
  StartRunResponse,
} from '../types/run'
import apiRequest, { ApiError } from './apiClient'

const RUN_SESSION_KEY = 'pokemon-14-0:active-run'

let startRunRequest: Promise<RunSession> | null = null

export function getRunHeaders(run: RunSession, authSession: AuthSession | null): HeadersInit {
  const headers: Record<string, string> = {}

  if (run.ownerType === 'account' && authSession?.accessToken) {
    headers.Authorization = `Bearer ${authSession.accessToken}`
  }
  if (run.ownerType === 'guest' && run.guestSessionToken) {
    headers['X-Guest-Session'] = run.guestSessionToken
  }

  return headers
}

function authHeaders(authSession: AuthSession | null): HeadersInit {
  return authSession ? { Authorization: `Bearer ${authSession.accessToken}` } : {}
}

export function getRunSession(): RunSession | null {
  const raw = window.sessionStorage.getItem(RUN_SESSION_KEY)
  if (!raw) return null

  try {
    const parsed = JSON.parse(raw) as RunSession
    if (
      typeof parsed.runId === 'string' &&
      (parsed.ownerType === 'account' || parsed.ownerType === 'guest') &&
      (parsed.guestSessionToken === null || typeof parsed.guestSessionToken === 'string')
    ) {
      return parsed
    }
  } catch {
    window.sessionStorage.removeItem(RUN_SESSION_KEY)
  }

  return null
}

function storeRunSession(run: RunSession): RunSession {
  window.sessionStorage.setItem(RUN_SESSION_KEY, JSON.stringify(run))
  return run
}

export function clearRunSession(): void {
  window.sessionStorage.removeItem(RUN_SESSION_KEY)
}

export function abandonRun(run: RunSession, authSession: AuthSession | null): Promise<RunResponse> {
  return apiRequest<RunResponse>(`/runs/${run.runId}/abandon`, {
    method: 'POST',
    headers: getRunHeaders(run, authSession),
  })
}

async function readCurrentRun(run: RunSession, authSession: AuthSession | null): Promise<RunResponse> {
  return apiRequest<RunResponse>('/runs/current', {
    headers: getRunHeaders(run, authSession),
  })
}

async function createRun(authSession: AuthSession | null): Promise<RunSession> {
  const response = await apiRequest<StartRunResponse>('/runs', {
    method: 'POST',
    headers: authHeaders(authSession),
  })
  return storeRunSession({
    runId: response.id,
    ownerType: authSession ? 'account' : 'guest',
    guestSessionToken: response.guest_session_token,
  })
}

async function startOrResumeRunRequest(authSession: AuthSession | null): Promise<RunSession> {
  const storedRun = getRunSession()

  if (storedRun && (storedRun.ownerType === 'guest' || authSession)) {
    try {
      await readCurrentRun(storedRun, authSession)
      return storedRun
    } catch (error) {
      if (!(error instanceof ApiError) || ![401, 404].includes(error.status)) throw error
      clearRunSession()
    }
  }

  try {
    return await createRun(authSession)
  } catch (error) {
    if (!(error instanceof ApiError) || error.status !== 409) throw error

    const run = storeRunSession({
      runId: '',
      ownerType: authSession ? 'account' : 'guest',
      guestSessionToken: null,
    })
    try {
      const currentRun = await readCurrentRun(run, authSession)
      return storeRunSession({ ...run, runId: currentRun.id })
    } catch {
      clearRunSession()
      throw error
    }
  }
}

export function startOrResumeRun(authSession: AuthSession | null): Promise<RunSession> {
  if (startRunRequest) return startRunRequest

  startRunRequest = startOrResumeRunRequest(authSession)
  return startRunRequest.finally(() => {
    startRunRequest = null
  })
}

export function getDraftRound(run: RunSession, authSession: AuthSession | null): Promise<DraftRound> {
  return apiRequest<DraftRound>(`/runs/${run.runId}/draft`, {
    headers: getRunHeaders(run, authSession),
  })
}

export function rerollDraftRound(run: RunSession, authSession: AuthSession | null): Promise<DraftRound> {
  return apiRequest<DraftRound>(`/runs/${run.runId}/draft/reroll`, {
    method: 'POST',
    headers: getRunHeaders(run, authSession),
  })
}

export function selectDraftOption(
  run: RunSession,
  authSession: AuthSession | null,
  option: DraftOption,
): Promise<DraftSelection> {
  return apiRequest<DraftSelection>(`/runs/${run.runId}/draft/selection`, {
    method: 'POST',
    headers: getRunHeaders(run, authSession),
    body: JSON.stringify({ option_number: option.option_number }),
  })
}

export function getRunTeam(run: RunSession, authSession: AuthSession | null): Promise<RunTeamMember[]> {
  return apiRequest<RunTeamMember[]>(`/runs/${run.runId}/team`, {
    headers: getRunHeaders(run, authSession),
  })
}

export function getRunOutcome(run: RunSession, authSession: AuthSession | null): Promise<RunOutcome> {
  return apiRequest<RunOutcome>(`/runs/${run.runId}/result`, {
    headers: getRunHeaders(run, authSession),
  })
}

export function challengePreviousChampion(
  run: RunSession,
  authSession: AuthSession | null,
): Promise<ChampionChallenge> {
  return apiRequest<ChampionChallenge>(`/runs/${run.runId}/champion-challenge`, {
    method: 'POST',
    headers: getRunHeaders(run, authSession),
  })
}

export function publishCompletedRunToRanking(
  run: RunSession,
  authSession: AuthSession,
): Promise<RunOutcome> {
  return apiRequest<RunOutcome>(`/runs/${run.runId}/ranking`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${authSession.accessToken}`,
      ...(run.guestSessionToken ? { 'X-Guest-Session': run.guestSessionToken } : {}),
    },
  })
}

export function storeClaimedRunSession(run: RunSession): RunSession {
  return storeRunSession({ ...run, ownerType: 'account', guestSessionToken: null })
}
