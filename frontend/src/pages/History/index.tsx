import PageContainer from '../../components/PageContainer'
import PageHeading from '../../components/PageHeading'

export default function HistoryPage() {
  return (
    <PageContainer>
      <PageHeading
        eyebrow="Suas runs"
        title="Histórico"
        description="Aqui aparecerão suas runs concluídas, derrotas e abandonos, com acesso aos respectivos resultados."
      />
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 text-slate-300">
        O histórico será conectado ao backend nesta página.
      </div>
    </PageContainer>
  )
}
