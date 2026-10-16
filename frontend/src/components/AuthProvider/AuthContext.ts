import { createContext } from 'react'
import type { AuthResponse, AuthSession } from '../../types/account'

export type AuthContextValue = {
  session: AuthSession | null
  signIn: (response: AuthResponse) => void
  signOut: () => void
}

export const AuthContext = createContext<AuthContextValue | null>(null)
