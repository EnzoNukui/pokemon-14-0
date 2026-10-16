import { FaChevronDown } from 'react-icons/fa'
import { TbPokeball } from 'react-icons/tb'
import { Link, NavLink } from 'react-router'
import { ROUTES } from '../../routes/paths'
import useAuth from '../AuthProvider/useAuth'

const navigation = [
  { to: ROUTES.home, label: 'Início', end: true },
  { to: ROUTES.play, label: 'Jogar' },
  { to: ROUTES.hallOfFame, label: 'Ranking' },
]

export default function Header() {
  const { session } = useAuth()

  return (
    <header className="px-4 pt-5 sm:px-8 sm:pt-7">
      <div className="mx-auto grid max-w-[90rem] grid-cols-[minmax(0,1fr)_auto] items-center gap-x-3 gap-y-2 rounded-2xl border-2 border-[#102f5b] bg-surface px-3 py-2.5 shadow-[0_3px_0_#102f5b] sm:px-5 sm:py-3 lg:grid-cols-[minmax(0,1fr)_1px_auto_1px_minmax(0,1fr)] lg:gap-x-4 lg:px-6">
        <Link
          aria-label="Pokémon 14-0, início"
          className="inline-flex min-w-0 items-center gap-2 rounded-lg sm:gap-2.5"
          to={ROUTES.home}
          title="Pokémon 14-0"
        >
          <span className="grid size-10 shrink-0 place-items-center rounded-full border-2 border-[#102f5b] bg-brand-soft text-brand-strong sm:size-11">
            <TbPokeball aria-hidden="true" className="text-2xl sm:text-[1.7rem]" />
          </span>
          <span className="whitespace-nowrap font-sans text-base font-bold tracking-tight text-graphite sm:text-xl">
            Pokémon 14-0
          </span>
        </Link>

        <span aria-hidden="true" className="hidden h-8 w-px bg-[#102f5b]/20 lg:block" />

        <nav aria-label="Navegação principal" className="col-span-2 row-start-2 flex items-center justify-center gap-1.5 lg:col-span-1 lg:col-start-3 lg:row-start-1 lg:gap-2">
          {navigation.map(({ to, label, end }) => (
            <NavLink
              end={end}
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex min-h-10 shrink-0 items-center justify-center whitespace-nowrap rounded-lg border-2 px-3 font-sans text-sm font-semibold transition-colors sm:min-h-11 sm:px-3.5 sm:text-base ${
                  isActive
                    ? 'border-brand bg-brand text-white shadow-[0_2px_0_#102f5b]'
                    : 'border-transparent text-graphite hover:bg-brand-soft hover:text-brand-strong'
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>

        <span aria-hidden="true" className="hidden h-8 w-px bg-[#102f5b]/20 lg:col-start-4 lg:row-start-1 lg:block" />

        {session ? (
          <span
            aria-label={`Conectado como ${session.user.trainer_name}`}
            className="col-start-2 row-start-1 flex min-h-10 max-w-36 items-center justify-self-end gap-1.5 rounded-lg border-2 border-[#102f5b]/25 px-2.5 text-graphite sm:min-h-11 sm:gap-2 sm:px-3 lg:col-start-5 lg:gap-2.5 lg:px-3.5"
          >
            <TbPokeball aria-hidden="true" className="shrink-0 text-lg text-brand-strong sm:text-xl" />
            <span className="truncate font-sans text-xs font-semibold sm:text-sm">{session.user.trainer_name}</span>
          </span>
        ) : (
          <Link
            aria-label="Entrar ou criar uma conta"
            className="col-start-2 row-start-1 flex min-h-10 items-center justify-self-end gap-1.5 rounded-lg border-2 border-[#102f5b]/25 px-2.5 text-graphite transition-colors hover:border-brand/50 hover:bg-brand-soft sm:min-h-11 sm:gap-2 sm:px-3 lg:col-start-5 lg:gap-2.5 lg:px-3.5"
            to={ROUTES.login}
          >
            <TbPokeball aria-hidden="true" className="shrink-0 text-lg text-brand-strong sm:text-xl" />
            <span className="whitespace-nowrap font-sans text-xs font-semibold sm:text-sm">Visitante</span>
            <FaChevronDown aria-hidden="true" className="shrink-0 text-[0.55rem]" />
          </Link>
        )}
      </div>
    </header>
  )
}
