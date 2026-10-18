import { useState, type FormEvent } from 'react'
import { FaChevronRight, FaEnvelope, FaLock, FaUser } from 'react-icons/fa'
import { useLocation, useNavigate } from 'react-router'
import AuthField from '../../components/AuthField/AuthField'
import AuthPanel from '../../components/AuthPanel/AuthPanel'
import useAuth from '../../components/AuthProvider/useAuth'
import { ROUTES } from '../../routes/paths'
import { getAuthErrorMessage, register } from '../../service/authService'

export default function RegisterPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { signIn } = useAuth()
  const [trainerName, setTrainerName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')

    if (password !== confirmPassword) {
      setError('As senhas não coincidem.')
      return
    }

    setIsSubmitting(true)
    try {
      const response = await register({
        trainer_name: trainerName.trim(),
        email: email.trim(),
        password,
      })
      signIn(response)
      const returnTo = (location.state as { returnTo?: unknown } | null)?.returnTo
      navigate(typeof returnTo === 'string' && returnTo.startsWith('/') ? returnTo : ROUTES.home)
    } catch (submitError) {
      setError(getAuthErrorMessage(submitError, 'register'))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <AuthPanel mode="register">
      <form className="space-y-3.5 sm:space-y-4" onSubmit={handleSubmit}>
        <AuthField
          autoComplete="nickname"
          id="register-trainer-name"
          icon={FaUser}
          label="Nome de treinador"
          maxLength={24}
          minLength={2}
          onChange={(event) => setTrainerName(event.target.value)}
          placeholder="Seu nome no jogo"
          required
          value={trainerName}
        />
        <AuthField
          autoComplete="email"
          id="register-email"
          icon={FaEnvelope}
          label="E-mail"
          onChange={(event) => setEmail(event.target.value)}
          placeholder="seu@email.com"
          required
          type="email"
          value={email}
        />
        <AuthField
          autoComplete="new-password"
          id="register-password"
          icon={FaLock}
          label="Senha"
          maxLength={128}
          minLength={8}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="Sua senha"
          required
          type="password"
          value={password}
        />
        <AuthField
          autoComplete="new-password"
          id="register-confirm-password"
          icon={FaLock}
          label="Confirmar senha"
          maxLength={128}
          onChange={(event) => setConfirmPassword(event.target.value)}
          placeholder="Digite a senha novamente"
          required
          type="password"
          value={confirmPassword}
        />

        {error && <p role="alert" className="m-0 rounded-md border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-800">{error}</p>}

        <button
          className="flex min-h-12 w-full items-center justify-center gap-3 rounded-lg border-[3px] border-[#102f5b] bg-brand px-5 font-display text-lg uppercase text-white shadow-[0_3px_0_#102f5b] transition-colors hover:bg-brand-strong disabled:cursor-wait disabled:opacity-70 sm:text-xl"
          disabled={isSubmitting}
          type="submit"
        >
          {isSubmitting ? 'Criando conta...' : 'Criar conta'}
          {!isSubmitting && <FaChevronRight aria-hidden="true" className="text-sm" />}
        </button>
      </form>
    </AuthPanel>
  )
}
