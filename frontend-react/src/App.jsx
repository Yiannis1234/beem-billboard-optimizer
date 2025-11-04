import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import Analytics from './pages/Analytics'

const Header = () => {
  const location = useLocation()
  const isHome = location.pathname === '/'

  return (
    <header className="sticky top-0 z-50 border-b border-blue-200 bg-gradient-to-r from-blue-600 to-cyan-600 shadow-lg">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-3 py-3 sm:px-4 sm:py-4 lg:px-6">
        <Link to="/" className="inline-flex items-center gap-2 transition hover:opacity-90 sm:gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-white shadow-lg sm:h-14 sm:w-14 sm:rounded-xl">
            <svg className="h-7 w-7 sm:h-10 sm:w-10" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 10L28 16V26L20 32L12 26V16L20 10Z" fill="#0078FF"/>
              <path d="M20 15L24 18V24L20 27L16 24V18L20 15Z" fill="white"/>
            </svg>
          </div>
          <div>
            <div className="text-xl font-black tracking-tight text-white sm:text-2xl lg:text-3xl">BritMetrics</div>
            <div className="hidden text-xs font-semibold text-blue-100 sm:block">Billboard Intelligence</div>
          </div>
        </Link>
        
        <nav className="flex items-center gap-1 sm:gap-2">
          <Link
            to="/"
            className={`rounded-lg px-2 py-1.5 text-xs font-semibold transition sm:rounded-xl sm:px-4 sm:py-2 sm:text-sm ${
              isHome
                ? 'bg-white text-blue-600 shadow-lg'
                : 'text-white hover:bg-white/10'
            }`}
          >
            <span className="hidden sm:inline">🎯 Campaign Planner</span>
            <span className="sm:hidden">🎯</span>
          </Link>
          <Link
            to="/analytics"
            className={`rounded-lg px-2 py-1.5 text-xs font-semibold transition sm:rounded-xl sm:px-4 sm:py-2 sm:text-sm ${
              !isHome
                ? 'bg-white text-blue-600 shadow-lg'
                : 'text-white hover:bg-white/10'
            }`}
          >
            <span className="hidden sm:inline">📊 Analytics</span>
            <span className="sm:hidden">📊</span>
          </Link>
        </nav>
      </div>
    </header>
  )
}

const Footer = () => (
  <footer className="border-t border-slate-200 bg-gradient-to-br from-slate-900 to-slate-800 px-4 py-8 text-slate-100 sm:px-6 sm:py-10 lg:px-10">
    <div className="mx-auto flex max-w-7xl flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <div className="flex items-center gap-2 sm:gap-3">
          <svg className="h-8 w-8 sm:h-10 sm:w-10" viewBox="0 0 40 40" fill="none">
            <rect width="40" height="40" rx="8" fill="white" fillOpacity="0.1"/>
            <path d="M20 10L28 16V26L20 32L12 26V16L20 10Z" fill="white"/>
            <path d="M20 15L24 18V24L20 27L16 24V18L20 15Z" fill="#0078FF"/>
          </svg>
          <div>
            <p className="text-base font-bold sm:text-lg">BritMetrics</p>
            <p className="text-xs text-slate-400 sm:text-sm">Billboard Intelligence Platform</p>
          </div>
        </div>
        <p className="mt-3 max-w-md text-xs text-slate-300 sm:mt-4 sm:text-sm">
          React + FastAPI powered platform for data-driven outdoor advertising decisions. Real-time weather, traffic, and audience insights.
        </p>
      </div>
      <div className="flex flex-col gap-2 sm:gap-3">
        <a
          href="mailto:vamvak@outlook.com"
          className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-white px-4 py-2.5 text-xs font-semibold text-slate-900 shadow-lg transition hover:-translate-y-0.5 hover:bg-slate-100 sm:w-auto sm:rounded-xl sm:px-5 sm:py-3 sm:text-sm"
        >
          📬 Contact BritMetrics
        </a>
        <a
          href="https://linkedin.com"
          target="_blank"
          rel="noreferrer"
          className="inline-flex w-full items-center justify-center gap-2 rounded-lg border border-white/20 px-4 py-2.5 text-xs font-semibold text-white transition hover:bg-white/10 sm:w-auto sm:rounded-xl sm:px-5 sm:py-3 sm:text-sm"
        >
          💼 LinkedIn
        </a>
      </div>
    </div>
    <div className="mx-auto mt-6 max-w-7xl border-t border-slate-700 pt-4 text-center text-xs text-slate-400 sm:mt-8 sm:pt-6">
      © 2025 BritMetrics. Built with React, Vite, Tailwind CSS & FastAPI.
    </div>
  </footer>
)

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen flex-col">
        <Header />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  )
}

export default App
