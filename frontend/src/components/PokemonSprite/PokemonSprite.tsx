import { useState } from 'react'

type PokemonSpriteProps = {
  name: string
  pokedexNumber?: number
  spriteUrl?: string | null
  size?: 'team' | 'compact' | 'normal' | 'battle'
  side?: 'front' | 'back'
}

export default function PokemonSprite({ name, pokedexNumber, spriteUrl, size = 'normal', side = 'front' }: PokemonSpriteProps) {
  const [useFallback, setUseFallback] = useState(false)
  const fallback = pokedexNumber
    ? `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${side === 'back' ? 'back/' : ''}${pokedexNumber}.png`
    : null
  const source = useFallback ? fallback : spriteUrl ?? fallback
  if (!source) return null

  return (
    <img
      alt={name}
      className={`relative z-10 object-contain [image-rendering:pixelated] ${size === 'team' ? 'size-7 sm:size-10' : size === 'compact' ? 'size-12 sm:size-16' : size === 'battle' ? 'h-44 w-44 sm:h-64 sm:w-64' : 'size-24 sm:size-28'}`}
      decoding="async"
      loading="lazy"
      src={source}
      onError={() => {
        if (spriteUrl && fallback && spriteUrl !== fallback && !useFallback) setUseFallback(true)
      }}
    />
  )
}
