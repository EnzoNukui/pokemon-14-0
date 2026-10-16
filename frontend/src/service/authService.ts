import apiRequest from './apiClient'
import { ApiError } from './apiClient'
import type { AuthResponse, AuthSession, LoginCredentials, RegistrationDetails } from '../types/account'

const AUTH_SESSION_KEY = 'pokemon-14-0:auth-session'

export async function login(credentials: LoginCredentials): Promise<AuthResponse> {
  return apiRequest<AuthResponse>('/accounts/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  })
}

export async function register(details: RegistrationDetails): Promise<AuthResponse> {
  return apiRequest<AuthResponse>('/accounts/register', {
    method: 'POST',
    body: JSON.stringify(details),
  })
}

export function storeAuthSession(response: AuthResponse): AuthSession {
  const session = { accessToken: response.access_token, user: response.user }
  window.sessionStorage.setItem(AUTH_SESSION_KEY, JSON.stringify(session))
  return session
}

export function getAuthSession(): AuthSession | null {
  const rawSession = window.sessionStorage.getItem(AUTH_SESSION_KEY)
  if (!rawSession) return null

  try {
    const session = JSON.parse(rawSession) as AuthSession
    if (session.accessToken && session.user?.id && session.user.trainer_name) return session
  } catch {
    window.sessionStorage.removeItem(AUTH_SESSION_KEY)
  }

  return null
}

export function clearAuthSession(): void {
  window.sessionStorage.removeItem(AUTH_SESSION_KEY)
}

export function getAuthErrorMessage(error: unknown, mode: 'login' | 'register'): string {
  if (!(error instanceof ApiError)) return 'Ocorreu um erro inesperado. Tente novamente.'

  if (error.status === 0) return error.message
  if (error.status === 401) return 'E-mail ou senha incorretos.'
  if (error.status === 409) return 'Este e-mail já possui uma conta.'
  if (error.status === 422) {
    return mode === 'register'
      ? 'Confira os dados. A senha precisa ter entre 8 e 128 caracteres.'
      : 'Informe um e-mail válido e uma senha.'
  }
  if (error.status === 503) return 'O acesso está temporariamente indisponível. Tente novamente mais tarde.'
  return 'Não foi possível concluir o acesso. Tente novamente.'
}
