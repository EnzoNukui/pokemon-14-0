import { FaChevronRight } from 'react-icons/fa'

const stages = [
  { number: '01', title: 'Draft', detail: '6 Pokémon', color: 'bg-brand' },
  { number: '02', title: 'Desafio', detail: '13 treinadores', color: 'bg-[#1684c7]' },
  { number: '03', title: 'Conquista', detail: 'Título de campeão', color: 'bg-[#f3a900]' },
]

export default function RunProgress() {
  return (
    <section id="run-progress" aria-label="Etapas da run" className="mx-auto w-full max-w-[90rem] px-4 sm:px-8">
      <ol className="m-0 grid list-none overflow-hidden rounded-xl border-[3px] border-[#102f5b] bg-white p-2 shadow-[0_3px_0_#102f5b] sm:grid-cols-3 sm:p-3">
        {stages.map((stage, index) => (
          <li
            key={stage.number}
            className={`relative flex min-h-20 items-center gap-3 px-3 py-2 sm:gap-5 sm:px-5 ${
              index < stages.length - 1 ? 'border-b-2 border-[#24639a]/30 sm:border-b-0 sm:border-r-2' : ''
            }`}
          >
            <span className={`grid size-12 shrink-0 rotate-45 place-items-center rounded-lg border-[3px] border-[#102f5b] ${stage.color} text-white shadow-[0_2px_0_#102f5b] sm:size-14`}>
              <span className="-rotate-45 font-[Impact,Arial_Narrow,sans-serif] text-xl sm:text-2xl">{stage.number}</span>
            </span>
            <div className="min-w-0">
              <p className="m-0 font-[Impact,Arial_Narrow,sans-serif] text-xl uppercase leading-none text-[#102f5b] sm:text-2xl">
                {stage.title}
              </p>
              <p className="m-0 mt-1 font-sans text-sm font-bold uppercase leading-tight text-[#4c80ae] sm:text-base">
                {stage.detail}
              </p>
            </div>
            {index < stages.length - 1 && (
              <FaChevronRight aria-hidden="true" className="ml-auto hidden shrink-0 text-xl text-[#102f5b] sm:block" />
            )}
          </li>
        ))}
      </ol>
    </section>
  )
}
