import Footer from './components/Footer'
import Header from './components/Header'
import AppRoutes from './routes'

export default function App() {
  return (
    <div className="flex min-h-screen flex-col bg-slate-950 text-slate-100">
      <Header />
      <main className="flex-1">
        <AppRoutes />
      </main>
      <Footer />
    </div>
  )
}
