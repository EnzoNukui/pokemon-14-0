import type { ReactNode } from 'react'
import { FaSignal } from 'react-icons/fa'
import { TbPokeball } from 'react-icons/tb'
import { Link, useLocation } from 'react-router'
import { ROUTES } from '../../routes/paths'

type AuthPanelProps = {
  mode: 'login' | 'register'
  children: ReactNode
}

export default function AuthPanel({ mode, children }: AuthPanelProps) {
  const isLogin = mode === 'login'
  const location = useLocation()

  return (
    <section className="mx-auto w-full max-w-5xl px-4 py-8 sm:px-8 sm:py-10">
      <div className="grid overflow-hidden rounded-2xl border-[3px] border-[#102f5b] bg-[#fffaf0] shadow-[0_5px_0_#102f5b] md:grid-cols-[12rem_minmax(0,1fr)] lg:grid-cols-[15rem_minmax(0,1fr)]">
        <aside aria-hidden="true" className="relative hidden min-h-[34rem] overflow-hidden border-r-[5px] border-[#102f5b] bg-brand md:block">
          <div className="absolute left-1/2 top-10 grid size-36 -translate-x-1/2 place-items-center rounded-full border-[7px] border-[#102f5b] bg-[#fffaf0] shadow-[inset_0_0_0_5px_#d7d9dc,0_4px_0_#102f5b] lg:size-44">
            <span className="absolute inset-x-0 top-1/2 h-2 -translate-y-1/2 bg-[#102f5b]" />
            <TbPokeball className="relative z-10 rounded-full bg-[#fffaf0] text-[5.8rem] text-brand-strong lg:text-[7rem]" />
          </div>
          <div className="absolute left-1/2 top-[15.5rem] grid size-24 -translate-x-1/2 grid-cols-3 grid-rows-3 lg:top-[18rem]">
            <span className="col-start-2 row-start-1 rounded-t bg-[#102f5b] shadow-[inset_0_2px_0_#52627a]" />
            <span className="col-start-1 row-start-2 rounded-l bg-[#102f5b] shadow-[inset_0_2px_0_#52627a]" />
            <span className="col-start-2 row-start-2 bg-[#263d60]" />
            <span className="col-start-3 row-start-2 rounded-r bg-[#102f5b] shadow-[inset_0_2px_0_#52627a]" />
            <span className="col-start-2 row-start-3 rounded-b bg-[#102f5b] shadow-[inset_0_2px_0_#52627a]" />
          </div>
          <div className="absolute bottom-20 left-1/2 flex -translate-x-1/2 gap-5">
            <span className="size-12 rounded-full border-4 border-[#102f5b] bg-[#182c4b] shadow-[inset_0_3px_0_#50617b]" />
            <span className="size-12 rounded-full border-4 border-[#102f5b] bg-[#182c4b] shadow-[inset_0_3px_0_#50617b]" />
          </div>
          <div className="absolute bottom-6 left-1/2 flex -translate-x-1/2 gap-1.5" aria-hidden="true">
            <span className="h-1 w-5 rounded-full bg-[#102f5b]" />
            <span className="h-1 w-5 rounded-full bg-[#102f5b]" />
            <span className="h-1 w-5 rounded-full bg-[#102f5b]" />
          </div>
        </aside>

        <div className="min-w-0 bg-[#c8d1ce] p-2 sm:p-3">
          <div className="relative h-full min-w-0 rounded-xl border-[5px] border-[#102f5b] bg-[#fffaf0] p-4 shadow-[inset_0_0_0_3px_#dce3da] sm:p-6 lg:p-7">
            <span aria-hidden="true" className="absolute left-2 top-2 size-2 rounded-full bg-[#8797a1] shadow-[inset_0_1px_1px_#536475]" />
            <span aria-hidden="true" className="absolute right-2 top-2 size-2 rounded-full bg-[#8797a1] shadow-[inset_0_1px_1px_#536475]" />
            <div className="mb-5 flex items-center gap-3 border-b-2 border-[#102f5b] pb-3 sm:mb-6">
              <TbPokeball aria-hidden="true" className="shrink-0 text-3xl text-brand-strong" />
              <h1 className="m-0 flex-1 font-display text-xl uppercase leading-none text-[#102f5b] sm:text-2xl">
                {isLogin ? 'Acesso de treinador' : 'Novo registro'}
              </h1>
              <FaSignal aria-hidden="true" className="shrink-0 text-lg text-[#42865a]" />
            </div>

            <nav aria-label="Alternar entre entrar e criar conta" className="mb-5 grid grid-cols-2 sm:mb-6">
              <Link
                aria-current={isLogin ? 'page' : undefined}
                className={`flex min-h-11 items-center justify-center rounded-l-md border-2 border-[#102f5b] px-3 font-display text-base uppercase transition-colors sm:text-lg ${isLogin ? 'bg-brand text-white' : 'bg-[#e9e6df] text-[#102f5b] hover:bg-brand-soft'}`}
                state={location.state}
                to={ROUTES.login}
              >
                Entrar
              </Link>
              <Link
                aria-current={!isLogin ? 'page' : undefined}
                className={`-ml-0.5 flex min-h-11 items-center justify-center rounded-r-md border-2 border-[#102f5b] px-3 font-display text-base uppercase transition-colors sm:text-lg ${!isLogin ? 'bg-brand text-white' : 'bg-[#e9e6df] text-[#102f5b] hover:bg-brand-soft'}`}
                state={location.state}
                to={ROUTES.register}
              >
                Criar conta
              </Link>
            </nav>

            {children}
          </div>
        </div>
      </div>

      <p className="mb-0 mt-5 flex items-center justify-center gap-2 text-center text-sm text-[#102f5b] sm:mt-6 sm:text-base">
        <span aria-hidden="true" className="size-3 shrink-0 rounded-full border border-[#102f5b] bg-[#4eae69] shadow-[0_0_0_2px_#cfe8d4]" />
        <span>Você pode jogar sem conta. Entre para registrar sua run no ranking.</span>
      </p>
    </section>
  )
}
