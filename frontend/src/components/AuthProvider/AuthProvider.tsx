import { useState, type ReactNode } from 'react'
import type { AuthResponse, AuthSession } from '../../types/account'
import { clearAuthSession, getAuthSession, storeAuthSession } from '../../service/authService'
import { AuthContext } from './AuthContext'

export default function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<AuthSession | null>(getAuthSession)

  function signIn(response: AuthResponse) {
    setSession(storeAuthSession(response))
  }

  function signOut() {
    clearAuthSession()
    setSession(null)
  }

  return <AuthContext.Provider value={{ session, signIn, signOut }}>{children}</AuthContext.Provider>
}

