export type AccountUser = {
  id: string
  trainer_name: string
  email: string
  created_at: string
}

export type AuthResponse = {
  access_token: string
  token_type: 'bearer'
  expires_in: number
  user: AccountUser
}

export type LoginCredentials = {
  email: string
  password: string
}

export type RegistrationDetails = LoginCredentials & {
  trainer_name: string
}

export type AuthSession = {
  accessToken: string
  user: AccountUser
}
