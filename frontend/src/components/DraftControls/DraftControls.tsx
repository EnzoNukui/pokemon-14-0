type DraftControlsProps = {
  canSelect: boolean
  canReroll: boolean
  busyAction: 'select' | 'reroll' | null
  onSelect: () => void
  onReroll: () => void
}

export default function DraftControls({
  canSelect,
  canReroll,
  busyAction,
  onSelect,
  onReroll,
}: DraftControlsProps) {
  return (
    <div className="mt-5 flex flex-col items-center gap-2 sm:mt-6">
      <div className="flex w-full max-w-[29rem] flex-col justify-center gap-3 sm:flex-row sm:gap-4">
        <button
          className="min-h-12 flex-1 border-[3px] border-graphite bg-brand px-5 font-display text-lg uppercase text-white shadow-[3px_3px_0_#35353a] transition enabled:hover:bg-brand-strong disabled:cursor-not-allowed disabled:border-graphite/60 disabled:bg-graphite-muted"
          disabled={!canSelect || busyAction !== null}
          onClick={onSelect}
          type="button"
        >
          {busyAction === 'select' ? 'Selecionando…' : 'Selecionar'}
        </button>
        <button
          className="min-h-12 flex-1 border-[3px] border-graphite bg-surface px-5 font-display text-lg uppercase text-graphite shadow-[3px_3px_0_#35353a] transition enabled:hover:bg-[#e9e2ce] disabled:cursor-not-allowed disabled:border-graphite/40 disabled:bg-surface/60 disabled:text-graphite/50"
          disabled={!canReroll || busyAction !== null}
          onClick={onReroll}
          type="button"
        >
          {busyAction === 'reroll' ? 'Girando…' : 'Rolar de novo'}
        </button>
      </div>
      <p className="m-0 flex items-center gap-3 font-display text-xs text-graphite sm:text-sm">
        <span aria-hidden="true" className="h-0.5 w-7 bg-brand" />
        1 uso por run
        <span aria-hidden="true" className="h-0.5 w-7 bg-brand" />
      </p>
    </div>
  )
}
