import { useEffect, useState } from 'react'
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import api from '../lib/api'

const COLORS = ['#0078FF', '#00C853', '#FF6B6B', '#FFA500', '#9C27B0', '#00BCD4']

const formatNumber = (value) => {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return '--'
  }
  return new Intl.NumberFormat('en-GB').format(value)
}

export default function Analytics() {
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [resetting, setResetting] = useState(false)

  const fetchAnalytics = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await api.fetchAnalytics()
      setAnalytics(data)
    } catch (err) {
      setError(err.message || 'Failed to load analytics')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = async () => {
    if (!window.confirm('Are you sure you want to reset all analyses? This cannot be undone.')) {
      return
    }
    
    try {
      setResetting(true)
      await api.clearAnalytics()
      await fetchAnalytics() // Refresh after clearing
    } catch (err) {
      setError(err.message || 'Failed to reset analytics')
    } finally {
      setResetting(false)
    }
  }

  useEffect(() => {
    fetchAnalytics()
    // Refresh every 30 seconds
    const interval = setInterval(fetchAnalytics, 30000)
    return () => clearInterval(interval)
  }, [])
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50">
        <div className="text-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-purple-600 border-t-transparent mx-auto"></div>
          <p className="mt-4 text-sm text-slate-600">Loading analytics...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50">
        <div className="rounded-2xl border border-red-200 bg-red-50 p-6 text-center">
          <p className="text-sm font-semibold text-red-700">Error loading analytics</p>
          <p className="mt-2 text-xs text-red-600">{error}</p>
        </div>
      </div>
    )
  }

  const hasData = analytics && analytics.totalAnalyses > 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50 pb-12 sm:pb-16">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-3 py-6 sm:gap-8 sm:px-4 sm:py-8 lg:py-12">
        {/* Header */}
        <div className="flex items-center justify-between rounded-2xl bg-gradient-to-r from-purple-600 to-pink-600 p-4 shadow-xl sm:rounded-3xl sm:p-8">
          <div>
            <h1 className="text-2xl font-black text-white sm:text-3xl lg:text-4xl">Analytics Dashboard</h1>
            <p className="mt-2 text-sm text-purple-100 sm:text-base lg:text-lg">Deep insights into your campaign performance and audience reach</p>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleReset}
              disabled={resetting || !analytics || analytics.totalAnalyses === 0}
              className="inline-flex items-center gap-2 rounded-xl bg-white/20 px-4 py-2 text-xs font-semibold text-white backdrop-blur-sm transition hover:bg-white/30 disabled:cursor-not-allowed disabled:opacity-50 sm:px-5 sm:py-2.5 sm:text-sm"
            >
              {resetting ? (
                <>
                  <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></span>
                  <span>Resetting...</span>
                </>
              ) : (
                <>
                  <span>🗑️</span>
                  <span>Reset All</span>
                </>
              )}
            </button>
            <div className="hidden lg:block">
              <svg className="h-24 w-24" viewBox="0 0 100 100" fill="none">
                <circle cx="50" cy="50" r="45" fill="white" fillOpacity="0.2" />
                <path d="M30 70L40 50L50 60L60 40L70 55L80 30" stroke="white" strokeWidth="4" strokeLinecap="round" />
              </svg>
            </div>
          </div>
        </div>

        {!hasData ? (
          /* No Data Message */
          <div className="rounded-2xl border border-amber-200 bg-gradient-to-br from-amber-50 to-orange-50 p-4 shadow-lg sm:rounded-3xl sm:p-6">
            <h2 className="text-lg font-bold text-amber-900 sm:text-xl">📊 No Analytics Data Yet</h2>
            <p className="mt-2 text-xs font-medium text-amber-900 sm:text-sm">
              Run analyses on the Campaign Planner page to see real analytics here.
            </p>
            <div className="mt-4 rounded-xl border border-amber-200 bg-white p-3 sm:p-4">
              <p className="text-xs font-semibold text-slate-900 sm:text-sm">To view analytics:</p>
              <ol className="mt-2 list-decimal list-inside space-y-1 text-xs font-medium text-slate-800 sm:text-sm">
                <li>Go to the Campaign Planner page</li>
                <li>Select a campaign type, city, and area</li>
                <li>Run the analysis to generate real data</li>
                <li>Return here to see aggregated insights</li>
              </ol>
            </div>
          </div>
        ) : (
          <>
            {/* Key Metrics */}
            <div className="grid gap-4 sm:gap-6 md:grid-cols-2 lg:grid-cols-4">
              <div className="rounded-xl border border-blue-200 bg-gradient-to-br from-blue-500 to-cyan-500 p-4 shadow-lg sm:rounded-2xl sm:p-6">
                <div className="text-xs font-semibold uppercase tracking-wide text-blue-100 sm:text-sm">Total Analyses</div>
                <div className="mt-2 text-3xl font-black text-white sm:text-4xl">{formatNumber(analytics.totalAnalyses)}</div>
                <div className="mt-2 text-xs text-blue-100 sm:text-sm">Campaign analyses run</div>
              </div>
              <div className="rounded-xl border border-emerald-200 bg-gradient-to-br from-emerald-500 to-teal-500 p-4 shadow-lg sm:rounded-2xl sm:p-6">
                <div className="text-xs font-semibold uppercase tracking-wide text-emerald-100 sm:text-sm">Avg Success Score</div>
                <div className="mt-2 text-3xl font-black text-white sm:text-4xl">{analytics.averageSuccessScore}/100</div>
                <div className="mt-2 text-xs text-emerald-100 sm:text-sm">🎯 Average performance</div>
              </div>
              <div className="rounded-xl border border-violet-200 bg-gradient-to-br from-violet-500 to-purple-500 p-4 shadow-lg sm:rounded-2xl sm:p-6">
                <div className="text-xs font-semibold uppercase tracking-wide text-violet-100 sm:text-sm">Total Impressions</div>
                <div className="mt-2 text-3xl font-black text-white sm:text-4xl">{formatNumber(analytics.totalImpressions)}</div>
                <div className="mt-2 text-xs text-violet-100 sm:text-sm">Per hour across all</div>
              </div>
              <div className="rounded-xl border border-orange-200 bg-gradient-to-br from-orange-500 to-red-500 p-4 shadow-lg sm:rounded-2xl sm:p-6">
                <div className="text-xs font-semibold uppercase tracking-wide text-orange-100 sm:text-sm">Locations Analyzed</div>
                <div className="mt-2 text-3xl font-black text-white sm:text-4xl">{analytics.locationPerformance.length}</div>
                <div className="mt-2 text-xs text-orange-100 sm:text-sm">Unique locations</div>
              </div>
            </div>

            {/* Charts Section */}
            <div className="grid gap-4 sm:gap-6 lg:grid-cols-2">
              {/* Location Performance - Pie Chart */}
              {analytics.locationPerformance.length > 0 && (
                <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-lg sm:rounded-3xl sm:p-6">
                  <h2 className="text-lg font-bold text-slate-900 sm:text-xl">📍 Location Distribution</h2>
                  <p className="mt-1 text-xs text-slate-600 sm:text-sm">Footfall share across locations</p>
                  <div className="mt-4" style={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={analytics.locationPerformance}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ areaName, footfall }) => `${areaName}: ${formatNumber(footfall)}`}
                          outerRadius={100}
                          fill="#8884d8"
                          dataKey="footfall"
                        >
                          {analytics.locationPerformance.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip 
                          formatter={(value) => formatNumber(value)}
                          contentStyle={{ backgroundColor: 'white', border: '1px solid #e0e7ff', borderRadius: '8px', color: '#1e293b' }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  {/* Legend below chart */}
                  <div className="mt-4 grid grid-cols-1 gap-2 text-xs sm:grid-cols-2">
                    {analytics.locationPerformance.map((entry, index) => (
                      <div key={entry.areaName} className="flex items-center gap-2">
                        <div 
                          className="h-3 w-3 rounded-full flex-shrink-0" 
                          style={{ backgroundColor: COLORS[index % COLORS.length] }}
                        />
                        <span className="font-medium text-slate-700 truncate">{entry.areaName}</span>
                        <span className="text-slate-500 ml-auto">{entry.successScore}/100</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Campaign Performance - Pie Chart */}
              {analytics.campaignPerformance.length > 0 && (
                <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-lg sm:rounded-3xl sm:p-6">
                  <h2 className="text-lg font-bold text-slate-900 sm:text-xl">🎯 Campaign Distribution</h2>
                  <p className="mt-1 text-xs text-slate-600 sm:text-sm">Analysis distribution by campaign type</p>
                  <div className="mt-4" style={{ height: 350 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={analytics.campaignPerformance}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={({ campaign, successScore }) => `${campaign}: ${successScore}/100`}
                          outerRadius={100}
                          fill="#8884d8"
                          dataKey="count"
                        >
                          {analytics.campaignPerformance.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip 
                          formatter={(value) => `${value} analysis${value !== 1 ? 'es' : ''}`}
                          contentStyle={{ backgroundColor: 'white', border: '1px solid #e0e7ff', borderRadius: '8px', color: '#1e293b' }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  {/* Legend below chart */}
                  <div className="mt-4 grid grid-cols-1 gap-2 text-xs sm:grid-cols-2">
                    {analytics.campaignPerformance.map((entry, index) => (
                      <div key={entry.campaign} className="flex items-center gap-2">
                        <div 
                          className="h-3 w-3 rounded-full flex-shrink-0" 
                          style={{ backgroundColor: COLORS[index % COLORS.length] }}
                        />
                        <span className="font-medium text-slate-700 truncate">{entry.campaign}</span>
                        <span className="text-slate-500 ml-auto">{entry.successScore}/100</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </>
        )}

        {/* Platform Info */}
        <div className="rounded-2xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-4 shadow-lg sm:rounded-3xl sm:p-8">
          <h2 className="text-xl font-bold text-slate-900 sm:text-2xl">🚀 About BritMetrics</h2>
          <p className="mt-3 text-xs text-slate-700 sm:mt-4 sm:text-sm lg:text-base">
            BritMetrics uses real-time data from multiple sources to provide accurate campaign forecasting
            and audience insights for outdoor advertising across UK cities.
          </p>
          <div className="mt-4 grid gap-3 sm:mt-6 sm:gap-4 md:grid-cols-3">
            <div className="rounded-lg border border-blue-200 bg-blue-50 p-3 sm:rounded-xl sm:p-4">
              <div className="text-2xl font-black text-blue-600 sm:text-3xl">10+</div>
              <div className="mt-1 text-xs font-semibold text-slate-700 sm:text-sm">Campaign Types</div>
            </div>
            <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 sm:rounded-xl sm:p-4">
              <div className="text-2xl font-black text-emerald-600 sm:text-3xl">20+</div>
              <div className="mt-1 text-xs font-semibold text-slate-700 sm:text-sm">UK Locations</div>
            </div>
            <div className="rounded-lg border border-purple-200 bg-purple-50 p-3 sm:rounded-xl sm:p-4">
              <div className="text-2xl font-black text-purple-600 sm:text-3xl">24/7</div>
              <div className="mt-1 text-xs font-semibold text-slate-700 sm:text-sm">Real-Time Updates</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

