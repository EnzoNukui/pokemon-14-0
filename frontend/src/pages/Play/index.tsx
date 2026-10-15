import ActionLink from '../../components/Buttons/ActionLink'
import PageContainer from '../../components/PageContainer'
import PageHeading from '../../components/PageHeading'
import { ROUTES } from '../../routes/paths'

export default function PlayPage() {
  return (
    <PageContainer>
      <PageHeading
        eyebrow="Sua run"
        title="Iniciar ou continuar"
        description="Este será o ponto de entrada da run. Ele verificará se existe uma run ativa e abrirá o draft ou a batalha correspondente."
      />
      <div className="flex flex-wrap gap-3">
        <ActionLink to={ROUTES.draft}>Ir para o draft</ActionLink>
        <ActionLink to={ROUTES.battle} variant="secondary">
          Ir para a batalha
        </ActionLink>
      </div>
    </PageContainer>
  )
}
