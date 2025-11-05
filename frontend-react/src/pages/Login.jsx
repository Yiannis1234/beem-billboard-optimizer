import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../lib/api'

export default function Login() {
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const handleFreeTrial = async () => {
    if (!email || !email.includes('@')) {
      setError('Please enter a valid email address')
      return
    }

    try {
      setLoading(true)
      setError(null)
      
      // Create free trial account
      const response = await api.createAccount({ email, trial: true })
      
      // Store auth token
      localStorage.setItem('britmetrics_auth', response.token)
      localStorage.setItem('britmetrics_email', email)
      localStorage.setItem('britmetrics_trial', 'true')
      
      // Redirect to home
      navigate('/')
    } catch (err) {
      setError(err.message || 'Failed to create account. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handlePayment = async () => {
    if (!email || !email.includes('@')) {
      setError('Please enter a valid email address')
      return
    }

    try {
      setLoading(true)
      setError(null)
      
      // Create Stripe checkout session
      const response = await api.createCheckoutSession({ email })
      
      // Redirect to Stripe checkout
      window.location.href = response.checkoutUrl
    } catch (err) {
      setError(err.message || 'Failed to create payment session. Please try again.')
      setLoading(false)
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50 px-4 py-12">
      <div className="w-full max-w-md">
        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-2xl sm:p-10">
          {/* Logo */}
          <div className="mb-6 flex justify-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-600 shadow-lg">
              <svg className="h-10 w-10" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 10L28 16V26L20 32L12 26V16L20 10Z" fill="white"/>
                <path d="M20 15L24 18V24L20 27L16 24V18L20 15Z" fill="#0078FF"/>
              </svg>
            </div>
          </div>

          <h1 className="mb-2 text-center text-3xl font-black text-slate-900">Welcome to BritMetrics</h1>
          <p className="mb-8 text-center text-sm text-slate-600">
            Start planning your outdoor campaigns with confidence
          </p>

          {error && (
            <div className="mb-4 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          <div className="mb-6">
            <label htmlFor="email" className="mb-2 block text-sm font-semibold text-slate-700">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              className="w-full rounded-xl border-2 border-slate-200 px-4 py-3 text-base font-semibold shadow-sm transition focus:border-blue-500 focus:outline-none focus:ring-4 focus:ring-blue-100"
              disabled={loading}
            />
          </div>

          <div className="space-y-3">
            <button
              onClick={handleFreeTrial}
              disabled={loading}
              className="w-full rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 px-6 py-4 text-base font-bold text-white shadow-lg transition hover:-translate-y-0.5 hover:from-blue-700 hover:to-cyan-700 hover:shadow-blue-500/50 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
                  <span>Creating Account...</span>
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  <span className="text-xl">✨</span>
                  <span>Start Free Trial</span>
                </span>
              )}
            </button>

            <div className="relative my-4">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-slate-200"></div>
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-white px-2 text-slate-500">Or</span>
              </div>
            </div>

            <button
              onClick={handlePayment}
              disabled={loading}
              className="w-full rounded-xl border-2 border-slate-300 bg-white px-6 py-4 text-base font-semibold text-slate-700 shadow-lg transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <span className="flex items-center justify-center gap-2">
                <span className="text-xl">💳</span>
                <span>Subscribe Now</span>
              </span>
            </button>
          </div>

          <p className="mt-6 text-center text-xs text-slate-500">
            Free trial includes full access to all features. No credit card required.
          </p>
        </div>
      </div>
    </div>
  )
}

