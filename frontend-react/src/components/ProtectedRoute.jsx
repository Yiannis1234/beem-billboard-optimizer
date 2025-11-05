import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import api from '../lib/api'

export default function ProtectedRoute({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(null) // null = checking
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('britmetrics_auth')
      
      if (!token) {
        setIsAuthenticated(false)
        setIsLoading(false)
        return
      }

      // Verify token is still valid with backend
      try {
        const response = await api.checkAuth(token)
        // Update stored values in case they changed (e.g., trial -> paid)
        if (response.email) {
          localStorage.setItem('britmetrics_email', response.email)
          localStorage.setItem('britmetrics_trial', response.trial ? 'true' : 'false')
        }
        setIsAuthenticated(true)
      } catch (err) {
        // Token invalid, clear storage
        localStorage.removeItem('britmetrics_auth')
        localStorage.removeItem('britmetrics_email')
        localStorage.removeItem('britmetrics_trial')
        setIsAuthenticated(false)
      } finally {
        setIsLoading(false)
      }
    }

    checkAuth()
  }, [])

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="text-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent mx-auto"></div>
          <p className="mt-4 text-sm text-slate-600">Verifying authentication...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

