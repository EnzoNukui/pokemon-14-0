import type { RunStage, RunStatus, RunTeamMember } from './run'

export type BattlePokemon = {
  slot_number: number
  pokemon_id: string
  name: string
  form_name: string | null
  primary_type: string
  secondary_type: string | null
  front_sprite_url: string | null
  national_dex_number: number | null
  nature: string
  ability: string
  held_item: string | null
  moves: string[]
  evs: Record<string, number>
  ivs: Record<string, number>
}

export type BattleView = {
  id: string
  battle_number: number
  stage: RunStage
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'ABANDONED'
  trainer_id: string
  trainer_name: string
  trainer_sprite_url: string | null
  trainer_team_id: string
  team_key: string
  team_category: string
  simulator_result: 'WIN' | 'LOSS' | 'DRAW' | null
  run_result: 'WIN' | 'LOSS' | 'DRAW' | null
  request_snapshot: ShowdownRequest | null
  opponent_team: BattlePokemon[]
}

export type ShowdownMove = {
  move: string
  disabled?: boolean
  pp?: number
  maxpp?: number
  target?: string
}

export type ShowdownRequest = {
  active?: Array<{ moves?: ShowdownMove[]; trapped?: boolean }>
  forceSwitch?: boolean[]
  teamPreview?: boolean
  wait?: boolean
  side?: {
    name?: string
    pokemon?: Array<{
      ident: string
      details: string
      condition: string
      active: boolean
      fainted?: boolean
    }>
  }
}

export type BattleEvent = {
  event_type: string
  payload: Record<string, unknown>
}

export type BattleTurn = {
  battle_id: string
  battle_number: number
  status: 'RUNNING' | 'COMPLETED' | 'ABANDONED'
  request: ShowdownRequest | null
  choice_error: string | null
  events: BattleEvent[]
  simulator_result: 'WIN' | 'LOSS' | 'DRAW' | null
  run_result: 'WIN' | 'LOSS' | 'DRAW' | null
  run_status: RunStatus
  run_stage: RunStage
  progress_index: number
  next_battle_number: number | null
}

export type BattleRoster = {
  player: RunTeamMember[]
  opponent: BattlePokemon[]
}
