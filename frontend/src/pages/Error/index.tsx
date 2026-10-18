import { FaArrowRight, FaHouse } from 'react-icons/fa6'
import { TbPokeball } from 'react-icons/tb'
import { Link } from 'react-router'
import { ROUTES } from '../../routes/paths'

export default function ErrorPage() {
  return (
    <section
      aria-labelledby="error-title"
      className="mx-auto flex min-h-[58vh] w-full max-w-3xl items-center justify-center px-4 py-12 sm:px-8 sm:py-16"
    >
      <div className="w-full border-[3px] border-[#102f5b] bg-surface p-5 text-center shadow-[0_5px_0_#102f5b] sm:p-9">
        <div className="mx-auto grid size-20 place-items-center rounded-full border-[3px] border-[#102f5b] bg-brand-soft text-brand-strong shadow-[inset_0_0_0_5px_#fffaf0] sm:size-24">
          <TbPokeball aria-hidden="true" className="text-5xl sm:text-6xl" />
        </div>

        <p className="mb-0 mt-5 font-display text-sm uppercase tracking-[0.16em] text-brand-strong">
          Erro 404 · Rota não encontrada
        </p>
        <h1 id="error-title" className="mb-0 mt-2 font-display text-3xl uppercase leading-tight text-[#102f5b] sm:text-5xl">
          Você se perdeu!
        </h1>
        <p className="mx-auto mb-0 mt-3 max-w-lg text-base leading-relaxed text-[#536987] sm:text-lg">
          Esse caminho não existe. Volte ao início ou siga para uma nova jornada.
        </p>

        <div className="mt-7 flex flex-col justify-center gap-3 sm:flex-row">
          <Link
            className="inline-flex min-h-12 items-center justify-center gap-2 border-[3px] border-[#102f5b] bg-brand px-5 py-2 font-display text-sm uppercase text-white shadow-[0_3px_0_#102f5b] transition-colors hover:bg-brand-strong focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-strong"
            to={ROUTES.home}
          >
            <FaHouse aria-hidden="true" />
            Voltar ao início
          </Link>
          <Link
            className="inline-flex min-h-12 items-center justify-center gap-2 border-[3px] border-[#102f5b]/30 bg-white px-5 py-2 font-display text-sm uppercase text-[#102f5b] transition-colors hover:border-[#102f5b] hover:bg-[#102f5b]/5 focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-strong"
            to={ROUTES.play}
          >
            Começar uma run
            <FaArrowRight aria-hidden="true" />
          </Link>
        </div>
      </div>
    </section>
  )
}
