import BattleSpeedControl, { type BattleSpeed } from '../BattleSpeedControl/BattleSpeedControl'
import { FaCaretDown, FaPause, FaPlay } from 'react-icons/fa'

export type BattleDialogMessage = {
  text: string
  moveName?: string
  moveType?: string
}

type BattleDialogProps = {
  messages: BattleDialogMessage[]
  speed: BattleSpeed
  paused: boolean
  onSpeedChange: (speed: BattleSpeed) => void
  onPauseToggle: () => void
}

const moveTypeStyles: Record<string, { label: string; text: string; background: string; accent: string }> = {
  normal: { label: 'Normal', text: '#374151', background: '#f3f4f6', accent: '#6b7280' },
  fire: { label: 'Fogo', text: '#9a3412', background: '#ffedd5', accent: '#ea580c' },
  water: { label: 'Água', text: '#075985', background: '#e0f2fe', accent: '#0284c7' },
  electric: { label: 'Elétrico', text: '#713f12', background: '#fef9c3', accent: '#ca8a04' },
  grass: { label: 'Grama', text: '#166534', background: '#dcfce7', accent: '#16a34a' },
  ice: { label: 'Gelo', text: '#155e75', background: '#cffafe', accent: '#0891b2' },
  fighting: { label: 'Lutador', text: '#991b1b', background: '#fee2e2', accent: '#dc2626' },
  poison: { label: 'Veneno', text: '#6b21a8', background: '#f3e8ff', accent: '#9333ea' },
  ground: { label: 'Terra', text: '#78350f', background: '#fef3c7', accent: '#a16207' },
  flying: { label: 'Voador', text: '#1e40af', background: '#dbeafe', accent: '#2563eb' },
  psychic: { label: 'Psíquico', text: '#9d174d', background: '#fce7f3', accent: '#db2777' },
  bug: { label: 'Inseto', text: '#3f6212', background: '#ecfccb', accent: '#65a30d' },
  rock: { label: 'Pedra', text: '#57534e', background: '#e7e5e4', accent: '#78716c' },
  ghost: { label: 'Fantasma', text: '#5b21b6', background: '#ede9fe', accent: '#7c3aed' },
  dragon: { label: 'Dragão', text: '#3730a3', background: '#e0e7ff', accent: '#4f46e5' },
  dark: { label: 'Sombrio', text: '#292524', background: '#d6d3d1', accent: '#44403c' },
  steel: { label: 'Aço', text: '#334155', background: '#e2e8f0', accent: '#64748b' },
  fairy: { label: 'Fada', text: '#86198f', background: '#fae8ff', accent: '#c026d3' },
}

function renderMessage(message: BattleDialogMessage) {
  if (!message.moveName) return message.text

  const moveStart = message.text.indexOf(message.moveName)
  if (moveStart < 0) return message.text

  const moveEnd = moveStart + message.moveName.length
  const typeStyle = moveTypeStyles[message.moveType?.trim().toLocaleLowerCase() ?? ''] ?? {
    label: 'Tipo indisponível',
    text: '#374151',
    background: '#f3f4f6',
    accent: '#6b7280',
  }

  return (
    <>
      {message.text.slice(0, moveStart)}
      <span
        className="inline-flex max-w-full items-center gap-1.5 rounded-sm border-b-2 border-l-4 px-1 font-bold"
        style={{ color: typeStyle.text, backgroundColor: typeStyle.background, borderColor: typeStyle.accent }}
      >
        {message.moveName}
        <span aria-label={`tipo ${typeStyle.label}`} className="border-l border-current/35 pl-1.5 text-[0.62em] uppercase tracking-wide">
          {typeStyle.label}
        </span>
      </span>
      {message.text.slice(moveEnd)}
    </>
  )
}

export default function BattleDialog({ messages, speed, paused, onSpeedChange, onPauseToggle }: BattleDialogProps) {
  const recentMessages = messages.slice(-2)

  return (
    <section aria-label="Relato da batalha" className="relative border-[3px] border-graphite bg-paper p-3 shadow-[4px_4px_0_rgb(53_53_58_/_16%)] sm:p-5">
      <div className="pointer-events-none absolute inset-1 border border-graphite/15" />
      <div className="relative flex items-center justify-between gap-3">
        <ol aria-live="polite" aria-relevant="additions" className="m-0 flex min-h-20 min-w-0 flex-1 list-none flex-col justify-center gap-1 overflow-hidden p-1 pr-3 font-display text-base text-graphite sm:min-h-24 sm:pl-3 sm:text-xl">
        {recentMessages.length ? recentMessages.map((message, index) => (
          <li key={`${messages.length - recentMessages.length + index}-${message.text}`} className={`truncate ${index === recentMessages.length - 1 ? 'font-semibold text-graphite' : 'text-graphite-muted'}`}>
            {renderMessage(message)}
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
