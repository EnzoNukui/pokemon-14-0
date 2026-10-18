export type ChampionRankingPokemon = {
  pokemon_id: string
  pokemon_name: string
  front_sprite_url: string | null
  national_dex_number: number | null
}

export type ChampionRankingEntry = {
  id: string
  trainer_name: string
  completed_battles: number
  completed_at: string
  team: ChampionRankingPokemon[]
}
