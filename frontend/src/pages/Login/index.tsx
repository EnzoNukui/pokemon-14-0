import { Link } from 'react-router'
import PageContainer from '../../components/PageContainer'
import PageHeading from '../../components/PageHeading'
import { ROUTES } from '../../routes/paths'

export default function LoginPage() {
  return (
    <PageContainer>
      <section className="mx-auto max-w-xl rounded-2xl border border-slate-800 bg-slate-900 p-7 sm:p-10">
        <PageHeading
          eyebrow="Bem-vindo de volta"
          title="Entrar"
          description="A tela de autenticação ficará aqui. A conexão do formulário com o backend será feita em uma etapa própria."
        />
        <p className="text-sm text-slate-400">
          Ainda não tem conta?{' '}
          <Link className="font-semibold text-amber-300 hover:text-amber-200" to={ROUTES.register}>
            Criar conta
          </Link>
        </p>
      </section>
    </PageContainer>
  )
}
