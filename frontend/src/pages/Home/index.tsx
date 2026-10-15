import ActionLink from '../../components/Buttons/ActionLink'
import PageContainer from '../../components/PageContainer'
import PageHeading from '../../components/PageHeading'
import { ROUTES } from '../../routes/paths'

export default function HomePage() {
  return (
    <PageContainer>
      <section className="rounded-3xl border border-slate-800 bg-gradient-to-br from-slate-900 via-slate-900 to-amber-950/40 p-7 sm:p-12">
        <PageHeading
          eyebrow="Uma run. Treze batalhas."
          title="Sua jornada Pokémon começa aqui."
          description="Monte sua equipe no draft, enfrente os treinadores em sequência e tente chegar ao título de campeão."
        />
        <div className="flex flex-wrap gap-3">
          <ActionLink to={ROUTES.play}>Jogar agora</ActionLink>
          <ActionLink to={ROUTES.hallOfFame} variant="secondary">
            Ver Hall da Fama
          </ActionLink>
        </div>
      </section>
    </PageContainer>
  )
}
