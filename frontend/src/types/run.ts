export type RunStatus = 'ACTIVE' | 'COMPLETED' | 'FAILED' | 'ABANDONED'

export type RunStage = 'DRAFT' | 'GYM' | 'ELITE_FOUR' | 'CHAMPION' | 'RESULT'

export type RunResponse = {
  id: string
  status: RunStatus
  stage: RunStage
  progress_index: number
  reroll_used: boolean
  legendary_selected: boolean
  created_at: string
  ended_at: string | null
}

export type StartRunResponse = RunResponse & {
  guest_session_token: string | null
}

export type RunSession = {
  runId: string
  ownerType: 'account' | 'guest'
  guestSessionToken: string | null
}

export type DraftOption = {
  option_number: number
  pokemon_id: string
  name: string
  form_name: string | null
  primary_type: string
  secondary_type: string | null
  draft_tier: number | null
  is_legendary: boolean
  is_mythical: boolean
  is_pseudo_legendary: boolean
  front_sprite_url: string | null
  national_dex_number: number | null
}

export type DraftRound = {
  round_number: number
  display_set: number
  reroll_available: boolean
  legendary_selected: boolean
  options: DraftOption[]
}

export type DraftSelection = {
  round_number: number
  pokemon_id: string
  pokemon_name: string
  team_slot: number
  draft_complete: boolean
  legendary_selected: boolean
}

export type RunTeamMember = {
  slot_number: number
  pokemon_id: string
  pokemon_name: string
  primary_type: string
  secondary_type: string | null
  front_sprite_url: string | null
  back_sprite_url: string | null
  national_dex_number: number | null
  build_snapshot: Record<string, unknown>
}
