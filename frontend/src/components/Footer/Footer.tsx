import { Link } from 'react-router'
import { ROUTES } from '../../routes/paths'

export default function Footer() {
  return (
    <footer className="mt-auto px-4 pb-4 pt-8 sm:px-6">
      <div className="mx-auto grid max-w-7xl grid-cols-1 items-center gap-3 border-t border-border py-4 text-center sm:grid-cols-[auto_1fr] sm:text-left lg:grid-cols-[auto_1fr_auto] lg:gap-6">
        <Link className="font-display text-sm uppercase tracking-wide text-graphite hover:text-brand-strong" to={ROUTES.home}>
          Pokémon 14-0
        </Link>
        <nav aria-label="Navegação do rodapé" className="flex flex-wrap items-center justify-center gap-x-4 gap-y-1 text-sm text-graphite-muted sm:justify-end lg:justify-center">
          <Link className="hover:text-brand-strong" to={ROUTES.home}>Início</Link>
          <Link className="hover:text-brand-strong" to={ROUTES.play}>Jogar</Link>
          <Link className="hover:text-brand-strong" to={ROUTES.hallOfFame}>Ranking</Link>
        </nav>
        <p className="m-0 text-[0.8rem] text-graphite-muted lg:text-right">Projeto de fã, sem vínculo oficial.</p>
      </div>
    </footer>
  )
}
