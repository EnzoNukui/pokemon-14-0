import { useContext } from 'react'
import { AuthContext } from './AuthContext'

export default function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth precisa ser usado dentro de AuthProvider.')
  return context
}
