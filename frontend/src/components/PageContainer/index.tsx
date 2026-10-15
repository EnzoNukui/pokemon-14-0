import type { ReactNode } from 'react'

type PageContainerProps = {
  children: ReactNode
}

export default function PageContainer({ children }: PageContainerProps) {
  return <div className="mx-auto w-full max-w-7xl px-5 py-12 sm:py-16">{children}</div>
}
