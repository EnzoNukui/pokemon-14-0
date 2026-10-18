import apiRequest from './apiClient'
import type { ChampionRankingEntry } from '../types/championship'

export function getChampionRanking(limit = 5): Promise<ChampionRankingEntry[]> {
  return apiRequest<ChampionRankingEntry[]>(`/champions/ranking?limit=${limit}`)
}
