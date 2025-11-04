import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import Analytics from './pages/Analytics'

const Header = () => {
  const location = useLocation()
  const isHome = location.pathname === '/'

  return (
    <header className="sticky top-0 z-50 border-b border-blue-200 bg-gradient-to-r from-blue-600 to-cyan-600 shadow-lg">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 lg:px-6">
        <Link to="/" className="inline-flex items-center gap-3 transition hover:opacity-90">
          <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-white shadow-lg">
            <svg className="h-10 w-10" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 10L28 16V26L20 32L12 26V16L20 10Z" fill="#0078FF"/>
              <path d="M20 15L24 18V24L20 27L16 24V18L20 15Z" fill="white"/>
            </svg>
          </div>
          <div>
            <div className="text-3xl font-black tracking-tight text-white">BritMetrics</div>
            <div className="text-xs font-semibold text-blue-100">Billboard Intelligence</div>
          </div>
        </Link>
        
        <nav className="flex items-center gap-2">
          <Link
            to="/"
            className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
              isHome
                ? 'bg-white text-blue-600 shadow-lg'
                : 'text-white hover:bg-white/10'
            }`}
          >
            🎯 Campaign Planner
          </Link>
          <Link
            to="/analytics"
            className={`rounded-xl px-4 py-2 text-sm font-semibold transition ${
              !isHome
                ? 'bg-white text-blue-600 shadow-lg'
                : 'text-white hover:bg-white/10'
            }`}
          >
            📊 Analytics
          </Link>
        </nav>
      </div>
    </header>
  )
}

const Footer = () => (
  <footer className="border-t border-slate-200 bg-gradient-to-br from-slate-900 to-slate-800 px-6 py-10 text-slate-100 lg:px-10">
    <div className="mx-auto flex max-w-7xl flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <div className="flex items-center gap-3">
          <svg className="h-10 w-10" viewBox="0 0 40 40" fill="none">
            <rect width="40" height="40" rx="8" fill="white" fillOpacity="0.1"/>
            <path d="M20 10L28 16V26L20 32L12 26V16L20 10Z" fill="white"/>
            <path d="M20 15L24 18V24L20 27L16 24V18L20 15Z" fill="#0078FF"/>
          </svg>
          <div>
            <p className="text-lg font-bold">BritMetrics</p>
            <p className="text-sm text-slate-400">Billboard Intelligence Platform</p>
          </div>
        </div>
        <p className="mt-4 max-w-md text-sm text-slate-300">
          React + FastAPI powered platform for data-driven outdoor advertising decisions. Real-time weather, traffic, and audience insights.
        </p>
      </div>
      <div className="flex flex-col gap-3">
        <a
          href="mailto:vamvak@outlook.com"
          className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-900 shadow-lg transition hover:-translate-y-0.5 hover:bg-slate-100"
        >
          📬 Contact BritMetrics
        </a>
        <a
          href="https://linkedin.com"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-2 rounded-xl border border-white/20 px-5 py-3 text-sm font-semibold text-white transition hover:bg-white/10"
        >
          💼 LinkedIn
        </a>
      </div>
    </div>
    <div className="mx-auto mt-8 max-w-7xl border-t border-slate-700 pt-6 text-center text-xs text-slate-400">
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
