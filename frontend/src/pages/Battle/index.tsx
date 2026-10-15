import PageContainer from '../../components/PageContainer'
import PageHeading from '../../components/PageHeading'

export default function BattlePage() {
  return (
    <PageContainer>
      <PageHeading
        eyebrow="Batalha"
        title="Enfrente o próximo treinador."
        description="Esta tela reunirá a equipe do adversário, o campo de batalha, os comandos e o progresso pelas 13 lutas."
      />
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 text-slate-300">
        A interface da batalha será construída nesta página.
      </div>
    </PageContainer>
  )
}
