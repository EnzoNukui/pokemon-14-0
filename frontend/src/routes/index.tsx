import { Route, Routes } from 'react-router'
import BattlePage from '../pages/Battle'
import DraftPage from '../pages/Draft'
import ErrorPage from '../pages/Error'
import HallOfFamePage from '../pages/HallOfFame'
import HistoryPage from '../pages/History'
import HomePage from '../pages/Home'
import LoginPage from '../pages/Login'
import PlayPage from '../pages/Play'
import RegisterPage from '../pages/Register'
import ResultPage from '../pages/Result'
import { ROUTES } from './paths'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path={ROUTES.home} element={<HomePage />} />
      <Route path={ROUTES.login} element={<LoginPage />} />
      <Route path={ROUTES.register} element={<RegisterPage />} />
      <Route path={ROUTES.play} element={<PlayPage />} />
      <Route path={ROUTES.draft} element={<DraftPage />} />
      <Route path={ROUTES.battle} element={<BattlePage />} />
      <Route path={ROUTES.resultPattern} element={<ResultPage />} />
      <Route path={ROUTES.history} element={<HistoryPage />} />
      <Route path={ROUTES.hallOfFame} element={<HallOfFamePage />} />
      <Route path="*" element={<ErrorPage />} />
    </Routes>
  )
}
