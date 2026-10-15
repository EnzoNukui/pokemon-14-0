import { Link } from 'react-router'
import PageContainer from '../../components/PageContainer'
import PageHeading from '../../components/PageHeading'
import { ROUTES } from '../../routes/paths'

export default function RegisterPage() {
  return (
    <PageContainer>
      <section className="mx-auto max-w-xl rounded-2xl border border-slate-800 bg-slate-900 p-7 sm:p-10">
        <PageHeading
          eyebrow="Comece sua jornada"
          title="Criar conta"
          description="A tela de cadastro ficará aqui. O envio e a validação dos dados serão conectados ao backend depois."
        />
        <p className="text-sm text-slate-400">
          Já tem conta?{' '}
          <Link className="font-semibold text-amber-300 hover:text-amber-200" to={ROUTES.login}>
            Entrar
          </Link>
        </p>
      </section>
    </PageContainer>
  )
}
