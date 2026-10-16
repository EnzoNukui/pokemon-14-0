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
      ? 'rounded-lg border-2 border-[#102f5b] bg-brand px-7 py-3 text-xl uppercase !text-white shadow-[0_4px_0_#102f5b] hover:bg-brand-strong sm:px-9 sm:py-4 sm:text-2xl'
      : 'rounded-lg px-2 py-2 text-base uppercase text-[#102f5b] underline decoration-2 underline-offset-4 hover:text-brand-strong sm:text-lg'

  return (
    <Link
      className={`inline-flex items-center justify-center gap-2 font-[Impact,Arial_Narrow,sans-serif] tracking-wide transition-colors ${appearance}`}
      {...linkProps}
    >
      {children}
    </Link>
  )
}
