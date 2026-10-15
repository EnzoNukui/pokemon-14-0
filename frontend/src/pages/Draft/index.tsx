import PageContainer from '../../components/PageContainer'
import PageHeading from '../../components/PageHeading'

export default function DraftPage() {
  return (
    <PageContainer>
      <PageHeading
        eyebrow="Monte sua equipe"
        title="Draft de Pokémon"
        description="Esta página apresentará as opções de cada rodada, permitirá escolher seis Pokémon e mostrará quando o reroll estiver disponível."
      />
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 text-slate-300">
        A interface do draft será construída nesta página.
      </div>
    </PageContainer>
  )
}
