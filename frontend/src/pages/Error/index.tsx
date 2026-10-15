import { Link } from 'react-router'
import PageContainer from '../../components/PageContainer'

export default function ErrorPage() {
  return (
    <PageContainer>
      <section className="mx-auto max-w-xl py-12 text-center">
        <p className="text-sm font-bold uppercase tracking-[0.2em] text-amber-300">Erro 404</p>
        <h1 className="mt-4 text-4xl font-black text-white">Essa rota não existe.</h1>
        <p className="mt-4 text-slate-300">Volte para o início para continuar sua jornada.</p>
        <Link className="mt-8 inline-flex font-semibold text-amber-300 hover:text-amber-200" to="/">
          Voltar para o início
        </Link>
      </section>
    </PageContainer>
  )
}
