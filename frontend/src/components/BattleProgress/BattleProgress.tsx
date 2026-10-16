import { FaCrown, FaDumbbell, FaTrophy } from 'react-icons/fa'

type BattleProgressProps = {
  battleNumber: number
}

const milestones = [
  ...Array.from({ length: 8 }, (_, index) => ({ battle: index + 1, label: `GIN. ${index + 1}`, icon: FaDumbbell })),
  { battle: 9, label: 'ELITE 4', icon: FaTrophy },
  { battle: 13, label: 'CAMPEÃO', icon: FaCrown },
]

export default function BattleProgress({ battleNumber }: BattleProgressProps) {
  const phase = battleNumber <= 8
    ? { label: 'GINÁSIO', current: battleNumber, total: 8 }
    : battleNumber <= 12
      ? { label: 'ELITE 4', current: battleNumber - 8, total: 4 }
      : { label: 'CAMPEÃO', current: 1, total: 1 }

  return (
    <section aria-label="Progresso do desafio" className="mx-auto grid w-full max-w-[100rem] gap-3 border-b-[3px] border-graphite/75 bg-paper px-4 py-3 sm:grid-cols-[auto_1fr] sm:items-center sm:px-7">
      <div className="flex w-fit overflow-hidden border-2 border-graphite/70 bg-surface font-display uppercase text-graphite">
        <p className="m-0 border-r-2 border-graphite/30 px-3 py-2 text-sm sm:px-4 sm:text-base">
          {phase.label} <span className="text-brand-strong">{String(phase.current).padStart(2, '0')} / {String(phase.total).padStart(2, '0')}</span>
        </p>
        <p className="m-0 px-3 py-2 text-sm sm:px-4 sm:text-base">
          BATALHA <span className="text-brand-strong">{String(battleNumber).padStart(2, '0')} / 13</span>
        </p>
      </div>

      <ol className="relative m-0 flex min-w-0 list-none items-center justify-between gap-2 overflow-x-auto p-0 before:absolute before:left-5 before:right-5 before:top-3 before:h-[2px] before:bg-graphite/25 sm:before:top-3.5">
        {milestones.map(({ battle: milestone, label, icon: Icon }) => {
          const isEliteFour = milestone === 9
          const active = battleNumber === milestone || (isEliteFour && battleNumber >= 9 && battleNumber <= 12)
          const complete = isEliteFour ? battleNumber > 12 : battleNumber > milestone
          return (
            <li key={label} aria-current={active ? 'step' : undefined} className="relative z-10 flex shrink-0 flex-col items-center gap-1 bg-paper px-1">
              <Icon aria-hidden="true" className={`size-6 sm:size-7 ${active ? 'text-brand-strong' : complete ? 'text-accent-strong' : 'text-graphite/35'}`} />
              <span className={`font-display text-[0.62rem] uppercase sm:text-xs ${active ? 'text-brand-strong' : complete ? 'text-graphite' : 'text-graphite-muted'}`}>{label}</span>
            </li>
          )
        })}
      </ol>
    </section>
  )
}
