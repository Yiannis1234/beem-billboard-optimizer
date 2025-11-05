import { Navigate } from 'react-router-dom'

export default function ProtectedRoute({ children }) {
  const isAuthenticated = localStorage.getItem('britmetrics_auth') !== null

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return children
}

