export type BattleSpeed = 'slow' | 'normal' | 'fast'

type BattleSpeedControlProps = {
  value: BattleSpeed
  onChange: (speed: BattleSpeed) => void
}

const speeds: { value: BattleSpeed; label: string }[] = [
  { value: 'slow', label: '1×' },
  { value: 'normal', label: '2×' },
  { value: 'fast', label: '3×' },
]

export default function BattleSpeedControl({ value, onChange }: BattleSpeedControlProps) {
  return (
    <fieldset className="flex items-center gap-1 border-0 p-0">
      <legend className="sr-only">Velocidade das mensagens</legend>
      <span aria-hidden="true" className="mr-1 font-display text-[0.65rem] uppercase text-graphite-muted">Texto</span>
      {speeds.map((speed) => (
        <button
          key={speed.value}
          aria-pressed={value === speed.value}
          className={`min-w-8 border px-1.5 py-0.5 font-display text-xs ${value === speed.value ? 'border-brand-strong bg-brand text-white' : 'border-graphite/30 bg-surface text-graphite-muted hover:border-brand-strong'}`}
          onClick={() => onChange(speed.value)}
          type="button"
        >
          {speed.label}
        </button>
      ))}
    </fieldset>
  )
}
