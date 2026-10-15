import type { ReactNode } from 'react'
import { Link, type LinkProps } from 'react-router'

type ActionLinkProps = LinkProps & {
  children: ReactNode
  variant?: 'primary' | 'secondary'
}

export default function ActionLink({
  children,
  variant = 'primary',
  ...linkProps
}: ActionLinkProps) {
  const appearance =
    variant === 'primary'
      ? 'bg-amber-300 text-slate-950 hover:bg-amber-200'
      : 'border border-slate-600 text-slate-100 hover:border-slate-400 hover:bg-slate-800'

  return (
    <Link
      className={`inline-flex items-center justify-center rounded-lg px-5 py-3 font-semibold transition ${appearance}`}
      {...linkProps}
    >
      {children}
    </Link>
  )
}
