import PageContainer from '../../components/PageContainer'
import PageHeading from '../../components/PageHeading'

export default function HallOfFamePage() {
  return (
    <PageContainer>
      <PageHeading
        eyebrow="Campeonato"
        title="Hall da Fama"
        description="Esta página reunirá o campeão atual e o histórico de jogadores que concluíram as 13 batalhas."
      />
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 text-slate-300">
        O Hall da Fama será conectado ao backend nesta página.
      </div>
    </PageContainer>
  )
}
