const DEFAULT_API_URL = 'http://localhost:8000'
const API_BASE_URL = (import.meta.env.VITE_API_URL || DEFAULT_API_URL).replace(/\/$/, '')

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
}

export default api
