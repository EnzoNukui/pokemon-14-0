import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import { ApiError } from '../../service/apiClient'
import { startOrResumeRun } from '../../service/runService'
import { ROUTES } from '../../routes/paths'
import useAuth from '../../components/AuthProvider/useAuth'

export default function PlayPage() {
  const { session } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState<string | null>(null)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    let cancelled = false

    void startOrResumeRun(session).then(
      () => {
        if (!cancelled) navigate(ROUTES.draft, { replace: true })
      },
      (reason: unknown) => {
        if (cancelled) return
        setError(
          reason instanceof ApiError
            ? reason.message
            : 'Não foi possível iniciar a run. Tente novamente.',
        )
      },
    )

    return () => {
      cancelled = true
    }
  }, [attempt, navigate, session])

  return (
    <section className="mx-auto flex min-h-[55vh] w-full max-w-5xl items-center justify-center px-4 py-10 sm:px-8">
      <div className="w-full max-w-xl border-[3px] border-brand-strong bg-surface p-6 text-center shadow-[inset_0_0_0_3px_#35353a,4px_4px_0_rgb(53_53_58_/_16%)] sm:p-9">
        <h1 className="m-0 font-display text-2xl uppercase text-graphite sm:text-3xl">
          {error ? 'Não foi possível iniciar' : 'Preparando sua run'}
        </h1>
        {error ? (
          <>
            <p className="mb-0 mt-4 text-graphite-muted">{error}</p>
            <button
              className="mt-6 min-h-12 border-[3px] border-graphite bg-brand px-7 font-display uppercase text-white shadow-[3px_3px_0_#35353a] hover:bg-brand-strong"
              onClick={() => {
                setError(null)
                setAttempt((current) => current + 1)
              }}
              type="button"
            >
              Tentar novamente
            </button>
          </>
        ) : (
          <p aria-live="polite" className="mb-0 mt-4 text-graphite-muted">
            Conectando ao servidor…
          </p>
        )}
      </div>
    </section>
  )
}
