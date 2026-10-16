import Footer from './components/Footer/Footer'
import Header from './components/Header/Header'
import AuthProvider from './components/AuthProvider/AuthProvider'
import AppRoutes from './routes'

export default function App() {
  return (
    <AuthProvider>
      <div className="flex min-h-screen flex-col bg-paper text-graphite">
        <Header />
        <main className="flex-1">
          <AppRoutes />
        </main>
        <Footer />
      </div>
    </AuthProvider>
  )
}
