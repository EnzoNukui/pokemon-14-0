import { useState, type FormEvent } from 'react'
import { FaChevronRight, FaEnvelope, FaLock } from 'react-icons/fa'
import { Link, useLocation, useNavigate } from 'react-router'
import AuthField from '../../components/AuthField/AuthField'
import AuthPanel from '../../components/AuthPanel/AuthPanel'
import useAuth from '../../components/AuthProvider/useAuth'
import { ROUTES } from '../../routes/paths'
import { getAuthErrorMessage, login } from '../../service/authService'

export default function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { signIn } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)

    try {
      const response = await login({ email: email.trim(), password })
      signIn(response)
      const returnTo = (location.state as { returnTo?: unknown } | null)?.returnTo
      navigate(typeof returnTo === 'string' && returnTo.startsWith('/') ? returnTo : ROUTES.home)
    } catch (submitError) {
      setError(getAuthErrorMessage(submitError, 'login'))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <AuthPanel mode="login">
      <form className="space-y-4 sm:space-y-5" onSubmit={handleSubmit}>
        <AuthField
          autoComplete="email"
          id="login-email"
          icon={FaEnvelope}
          label="E-mail"
          onChange={(event) => setEmail(event.target.value)}
          placeholder="seu@email.com"
          required
          type="email"
          value={email}
        />
        <AuthField
          autoComplete="current-password"
          id="login-password"
          icon={FaLock}
          label="Senha"
          maxLength={128}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Sua senha"
          required
          type="password"
          value={password}
        />

        {error && <p role="alert" className="m-0 rounded-md border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-800">{error}</p>}

        <button
          className="flex min-h-12 w-full items-center justify-center gap-3 rounded-lg border-[3px] border-[#102f5b] bg-brand px-5 font-display text-lg uppercase text-white shadow-[0_3px_0_#102f5b] transition-colors hover:bg-brand-strong disabled:cursor-wait disabled:opacity-70 sm:text-xl"
          disabled={isSubmitting}
          type="submit"
        >
          {isSubmitting ? 'Entrando...' : 'Entrar'}
          {!isSubmitting && <FaChevronRight aria-hidden="true" className="text-sm" />}
        </button>

        <p className="mb-0 border-t border-[#102f5b]/30 pt-3 text-center text-sm text-[#102f5b] sm:pt-4 sm:text-base">
          Ainda não tem conta?{' '}
          <Link className="font-semibold text-[#145da0] underline underline-offset-2 hover:text-brand-strong" state={location.state} to={ROUTES.register}>
            Criar conta
          </Link>
        </p>
      </form>
    </AuthPanel>
  )
}
