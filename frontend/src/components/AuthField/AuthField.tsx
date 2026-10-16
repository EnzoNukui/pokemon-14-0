import { useState, type InputHTMLAttributes } from 'react'
import { FaEye, FaEyeSlash } from 'react-icons/fa'
import type { IconType } from 'react-icons'

type AuthFieldProps = InputHTMLAttributes<HTMLInputElement> & {
  label: string
  icon: IconType
}

export default function AuthField({ label, icon: Icon, id, type = 'text', ...inputProps }: AuthFieldProps) {
  const [passwordVisible, setPasswordVisible] = useState(false)
  const isPassword = type === 'password'
  const inputType = isPassword && passwordVisible ? 'text' : type

  return (
    <div className="space-y-1.5">
      <label htmlFor={id} className="block font-sans text-sm font-bold uppercase tracking-wide text-[#102f5b]">
        {label}
      </label>
      <div className="flex h-11 items-center gap-3 rounded-md border-2 border-[#102f5b] bg-[#fffdf8] px-3 transition-colors focus-within:border-brand focus-within:ring-2 focus-within:ring-brand/15">
        <Icon aria-hidden="true" className="shrink-0 text-base text-[#102f5b]" />
        <input
          {...inputProps}
          autoComplete={inputProps.autoComplete}
          className="h-full min-w-0 flex-1 border-0 bg-transparent font-sans text-base text-graphite outline-none placeholder:text-graphite-muted/80"
          id={id}
          type={inputType}
        />
        {isPassword && (
          <button
            aria-label={passwordVisible ? 'Ocultar senha' : 'Mostrar senha'}
            aria-pressed={passwordVisible}
            className="grid size-8 shrink-0 place-items-center rounded text-[#102f5b] hover:bg-brand-soft"
            onClick={() => setPasswordVisible((visible) => !visible)}
            type="button"
          >
            {passwordVisible ? <FaEyeSlash aria-hidden="true" /> : <FaEye aria-hidden="true" />}
          </button>
        )}
      </div>
    </div>
  )
}
