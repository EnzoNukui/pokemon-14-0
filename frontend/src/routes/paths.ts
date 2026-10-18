export const ROUTES = {
  home: '/',
  login: '/login',
  register: '/register',
  play: '/play',
  draft: '/play/draft',
  battle: '/play/battle',
  resultPattern: '/runs/:runId/result',
  resultForRun: (runId: string) => `/runs/${runId}/result`,
  hallOfFame: '/hall-of-fame',
} as const
