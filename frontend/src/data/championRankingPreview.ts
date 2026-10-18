import type { ChampionRankingEntry } from '../types/championship'

const previewTrainers: {
  id: string
  trainer_name: string
  team: [number, string][]
}[] = [
  {
    id: 'preview-trainer-1',
    trainer_name: 'MestreKanto',
    team: [
      [6, 'Charizard'], [9, 'Blastoise'], [3, 'Venusaur'],
      [65, 'Alakazam'], [94, 'Gengar'], [149, 'Dragonite'],
    ],
  },
  {
    id: 'preview-trainer-2',
    trainer_name: 'PikaStorm',
    team: [
      [25, 'Pikachu'], [130, 'Gyarados'], [143, 'Snorlax'],
      [94, 'Gengar'], [150, 'Mewtwo'], [212, 'Scizor'],
    ],
  },
  {
    id: 'preview-trainer-3',
    trainer_name: 'TreinadorRed',
    team: [
      [6, 'Charizard'], [130, 'Gyarados'], [135, 'Jolteon'],
      [59, 'Arcanine'], [131, 'Lapras'], [65, 'Alakazam'],
    ],
  },
]

export const championRankingPreview: ChampionRankingEntry[] = previewTrainers.map(
  (trainer, trainerIndex) => ({
    id: trainer.id,
    trainer_name: trainer.trainer_name,
    completed_battles: 13,
    completed_at: `2026-10-${15 - trainerIndex}T12:00:00Z`,
    team: trainer.team.map(([nationalDexNumber, pokemonName]) => ({
      pokemon_id: `preview-${trainer.id}-${nationalDexNumber}`,
      pokemon_name: pokemonName,
      front_sprite_url: null,
      national_dex_number: nationalDexNumber,
    })),
  }),
)
