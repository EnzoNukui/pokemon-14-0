import { FaGamepad, FaHistory, FaHome, FaSignInAlt, FaTrophy, FaUserPlus } from 'react-icons/fa'
import { NavLink } from 'react-router'
import { ROUTES } from '../../routes/paths'

const mainLinks = [
  { to: ROUTES.home, label: 'Início', icon: FaHome },
  { to: ROUTES.play, label: 'Jogar', icon: FaGamepad },
  { to: ROUTES.history, label: 'Histórico', icon: FaHistory },
  { to: ROUTES.hallOfFame, label: 'Hall da Fama', icon: FaTrophy },
]

export default function Header() {
  return (
    <header className="border-b border-slate-800 bg-slate-950/95">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-5 py-4">
        <NavLink className="text-lg font-black tracking-wide text-amber-300" to={ROUTES.home}>
          POKÉMON 13-0
        </NavLink>

        <nav aria-label="Navegação principal" className="flex flex-wrap items-center gap-2">
          {mainLinks.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              className={({ isActive }) =>
                `inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition ${
                  isActive
                    ? 'bg-slate-800 text-amber-300'
                    : 'text-slate-300 hover:bg-slate-900 hover:text-white'
                }`
              }
              to={to}
            >
              <Icon aria-hidden="true" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <NavLink
            className="inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm text-slate-300 transition hover:bg-slate-900 hover:text-white"
            to={ROUTES.login}
          >
            <FaSignInAlt aria-hidden="true" />
            Entrar
          </NavLink>
          <NavLink
            className="inline-flex items-center gap-2 rounded-lg bg-amber-300 px-3 py-2 text-sm font-semibold text-slate-950 transition hover:bg-amber-200"
            to={ROUTES.register}
          >
            <FaUserPlus aria-hidden="true" />
            Criar conta
          </NavLink>
        </div>
      </div>
    </header>
  )
}
