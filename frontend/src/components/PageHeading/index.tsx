type PageHeadingProps = {
  eyebrow?: string
  title: string
  description: string
}

export default function PageHeading({ eyebrow, title, description }: PageHeadingProps) {
  return (
    <div className="mb-8 max-w-3xl">
      {eyebrow && (
        <p className="mb-3 text-sm font-bold uppercase tracking-[0.2em] text-amber-300">
          {eyebrow}
        </p>
      )}
      <h1 className="text-3xl font-black tracking-tight text-white sm:text-5xl">{title}</h1>
      <p className="mt-4 text-base leading-7 text-slate-300 sm:text-lg">{description}</p>
    </div>
  )
}
