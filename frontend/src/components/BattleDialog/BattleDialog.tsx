import BattleSpeedControl, { type BattleSpeed } from '../BattleSpeedControl/BattleSpeedControl'
import { FaCaretDown, FaPause, FaPlay } from 'react-icons/fa'

type BattleDialogProps = {
  messages: string[]
  speed: BattleSpeed
  paused: boolean
  onSpeedChange: (speed: BattleSpeed) => void
  onPauseToggle: () => void
}

export default function BattleDialog({ messages, speed, paused, onSpeedChange, onPauseToggle }: BattleDialogProps) {
  const recentMessages = messages.slice(-2)

  return (
    <section aria-label="Relato da batalha" className="relative border-[3px] border-graphite bg-paper p-3 shadow-[4px_4px_0_rgb(53_53_58_/_16%)] sm:p-5">
      <div className="pointer-events-none absolute inset-1 border border-graphite/15" />
      <div className="relative flex items-center justify-between gap-3">
        <ol aria-live="polite" aria-relevant="additions" className="m-0 flex min-h-20 min-w-0 flex-1 list-none flex-col justify-center gap-1 overflow-hidden p-1 pr-3 font-display text-base text-graphite sm:min-h-24 sm:pl-3 sm:text-xl">
        {recentMessages.length ? recentMessages.map((message, index) => (
          <li key={`${messages.length - recentMessages.length + index}-${message}`} className={`truncate ${index === recentMessages.length - 1 ? 'font-semibold text-graphite' : 'text-graphite-muted'}`}>
            {message}
          </li>
        )) : <li className="my-auto text-graphite-muted">Preparando o primeiro turno…</li>}
        </ol>
        <div className="flex shrink-0 flex-col items-end gap-2">
          <button
            aria-pressed={paused}
            className="flex min-h-8 items-center gap-1.5 border border-graphite/35 bg-surface px-2 font-display text-xs uppercase text-graphite hover:border-brand-strong hover:text-brand-strong"
            onClick={onPauseToggle}
            type="button"
          >
            {paused ? <FaPlay aria-hidden="true" /> : <FaPause aria-hidden="true" />}
            {paused ? 'Continuar' : 'Pausar'}
          </button>
          <BattleSpeedControl value={speed} onChange={onSpeedChange} />
          <FaCaretDown aria-hidden="true" className="mr-1 text-xl text-graphite" />
        </div>
      </div>
    </section>
  )
}
