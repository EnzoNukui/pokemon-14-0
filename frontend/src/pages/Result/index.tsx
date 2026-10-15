import { useParams } from 'react-router'
import ActionLink from '../../components/Buttons/ActionLink'
import PageContainer from '../../components/PageContainer'
import PageHeading from '../../components/PageHeading'
import { ROUTES } from '../../routes/paths'

export default function ResultPage() {
  const { runId } = useParams<{ runId: string }>()

  return (
    <PageContainer>
      <PageHeading
        eyebrow="Fim da run"
        title="Resultado"
        description="Esta página mostrará o desfecho, a equipe usada e o resumo da run."
      />
      <div className="mb-6 rounded-2xl border border-slate-800 bg-slate-900 p-5 text-sm text-slate-300">
        Run selecionada: <span className="font-mono text-amber-300">{runId}</span>
      </div>
      <ActionLink to={ROUTES.history} variant="secondary">
        Ver histórico
      </ActionLink>
    </PageContainer>
  )
}
