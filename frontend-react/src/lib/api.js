// In production, use empty string for relative URLs (same domain as the site)
// In dev, use localhost:8000
const DEFAULT_API_URL = import.meta.env.DEV ? 'http://localhost:8000' : ''
const API_BASE_URL = (import.meta.env.VITE_API_URL !== undefined ? import.meta.env.VITE_API_URL : DEFAULT_API_URL).replace(/\/$/, '')

const defaultHeaders = {
  'Content-Type': 'application/json',
}

async function request(path, options = {}) {
  const url = `${API_BASE_URL}${path}`
  const fetchOptions = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...(options.headers ?? {}),
    },
  }

  const response = await fetch(url, fetchOptions)

  if (!response.ok) {
    let detail = response.statusText
    try {
      const payload = await response.json()
      detail = payload.detail || payload.message || detail
    } catch {
      // Ignore JSON parse errors and use default detail
    }
    throw new Error(detail || 'Request failed')
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

export const api = {
  async fetchCampaigns() {
    return request('/api/campaigns')
  },
  async fetchCities() {
    return request('/api/cities')
  },
  async predict({ cityId, areaId, campaignId }) {
    return request('/api/predict', {
      method: 'POST',
      body: JSON.stringify({ cityId, areaId, campaignId }),
    })
  },
  async fetchAnalytics() {
    return request('/api/analytics')
  },
  async clearAnalytics() {
    return request('/api/analytics', {
      method: 'DELETE',
    })
  },
  async createAccount({ email, trial }) {
    return request('/api/auth/create-account', {
      method: 'POST',
      body: JSON.stringify({ email, trial }),
    })
  },
  async createCheckoutSession({ email }) {
    return request('/api/auth/create-checkout', {
      method: 'POST',
      body: JSON.stringify({ email }),
    })
  },
  async verifySession(sessionId) {
    return request(`/api/auth/verify-session?session_id=${sessionId}`)
  },
}

export default api
