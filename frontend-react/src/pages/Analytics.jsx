import { Link } from 'react-router-dom'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#0078FF', '#00C853', '#FF6B6B', '#FFA500', '#9C27B0', '#00BCD4']

// Sample data for visualizations
const cityComparisonData = [
  { city: 'Manchester Albert Sq', footfall: 120000, successScore: 85, audienceMatch: 78 },
  { city: 'Manchester Deansgate', footfall: 95000, successScore: 72, audienceMatch: 65 },
  { city: 'London Oxford Circus', footfall: 180000, successScore: 92, audienceMatch: 88 },
  { city: 'London Piccadilly', footfall: 150000, successScore: 88, audienceMatch: 82 },
]

const demographicData = [
  { demographic: 'Young Professionals', percentage: 35 },
  { demographic: 'Students', percentage: 25 },
  { demographic: 'Tourists', percentage: 20 },
  { demographic: 'Commuters', percentage: 15 },
  { demographic: 'Locals', percentage: 5 },
]

const campaignPerformance = [
  { month: 'Jan', impressions: 450000, engagement: 78, roi: 245 },
  { month: 'Feb', impressions: 520000, engagement: 82, roi: 278 },
  { month: 'Mar', impressions: 580000, engagement: 85, roi: 312 },
  { month: 'Apr', impressions: 610000, engagement: 88, roi: 345 },
  { month: 'May', impressions: 680000, engagement: 91, roi: 398 },
  { month: 'Jun', impressions: 720000, engagement: 93, roi: 425 },
]

export default function Analytics() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50 pb-16">
      <div className="mx-auto flex max-w-7xl flex-col gap-8 px-4 py-8 lg:py-12">
        {/* Header */}
        <div className="flex items-center justify-between rounded-3xl bg-gradient-to-r from-purple-600 to-pink-600 p-8 shadow-xl">
          <div>
            <Link
              to="/"
              className="inline-flex items-center gap-2 rounded-xl bg-white/20 px-4 py-2 text-sm font-semibold text-white backdrop-blur-sm transition hover:bg-white/30"
            >
              ← Back to Campaign Planner
            </Link>
            <h1 className="mt-4 text-4xl font-black text-white">Analytics Dashboard</h1>
            <p className="mt-2 text-lg text-purple-100">Deep insights into your campaign performance and audience reach</p>
          </div>
          <div className="hidden lg:block">
            <svg className="h-24 w-24" viewBox="0 0 100 100" fill="none">
              <circle cx="50" cy="50" r="45" fill="white" fillOpacity="0.2" />
              <path d="M30 70L40 50L50 60L60 40L70 55L80 30" stroke="white" strokeWidth="4" strokeLinecap="round" />
            </svg>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-2xl border border-blue-200 bg-gradient-to-br from-blue-500 to-cyan-500 p-6 shadow-lg">
            <div className="text-sm font-semibold uppercase tracking-wide text-blue-100">Total Impressions</div>
            <div className="mt-2 text-4xl font-black text-white">3.56M</div>
            <div className="mt-2 text-sm text-blue-100">↑ 23% from last period</div>
          </div>
          <div className="rounded-2xl border border-emerald-200 bg-gradient-to-br from-emerald-500 to-teal-500 p-6 shadow-lg">
            <div className="text-sm font-semibold uppercase tracking-wide text-emerald-100">Avg Success Score</div>
            <div className="mt-2 text-4xl font-black text-white">86/100</div>
            <div className="mt-2 text-sm text-emerald-100">🎯 Excellent performance</div>
          </div>
          <div className="rounded-2xl border border-violet-200 bg-gradient-to-br from-violet-500 to-purple-500 p-6 shadow-lg">
            <div className="text-sm font-semibold uppercase tracking-wide text-violet-100">Campaign ROI</div>
            <div className="mt-2 text-4xl font-black text-white">325%</div>
            <div className="mt-2 text-sm text-violet-100">↑ 45% increase</div>
          </div>
          <div className="rounded-2xl border border-orange-200 bg-gradient-to-br from-orange-500 to-red-500 p-6 shadow-lg">
            <div className="text-sm font-semibold uppercase tracking-wide text-orange-100">Active Campaigns</div>
            <div className="mt-2 text-4xl font-black text-white">12</div>
            <div className="mt-2 text-sm text-orange-100">Across 8 locations</div>
          </div>
        </div>

        {/* Charts Section */}
        <div className="grid gap-6 lg:grid-cols-2">
          {/* City Comparison */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg">
            <h2 className="text-xl font-bold text-slate-900">📊 Location Performance</h2>
            <p className="mt-1 text-sm text-slate-600">Success scores and footfall by area</p>
            <div className="mt-6" style={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={cityComparisonData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="city" fontSize={12} />
                  <YAxis fontSize={12} />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="successScore" fill="#0078FF" name="Success Score" />
                  <Bar dataKey="audienceMatch" fill="#00C853" name="Audience Match %" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Demographic Distribution */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg">
            <h2 className="text-xl font-bold text-slate-900">👥 Audience Demographics</h2>
            <p className="mt-1 text-sm text-slate-600">Target audience breakdown</p>
            <div className="mt-6" style={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={demographicData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={(entry) => `${entry.demographic}: ${entry.percentage}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="percentage"
                  >
                    {demographicData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Campaign Trends */}
          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-lg lg:col-span-2">
            <h2 className="text-xl font-bold text-slate-900">📈 Campaign Performance Over Time</h2>
            <p className="mt-1 text-sm text-slate-600">Impressions and ROI trends (last 6 months)</p>
            <div className="mt-6" style={{ height: 300 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={campaignPerformance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" fontSize={12} />
                  <YAxis yAxisId="left" fontSize={12} />
                  <YAxis yAxisId="right" orientation="right" fontSize={12} />
                  <Tooltip />
                  <Legend />
                  <Line yAxisId="left" type="monotone" dataKey="impressions" stroke="#0078FF" strokeWidth={3} name="Impressions" />
                  <Line yAxisId="right" type="monotone" dataKey="roi" stroke="#00C853" strokeWidth={3} name="ROI %" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Platform Info */}
        <div className="rounded-3xl border border-slate-200 bg-gradient-to-br from-slate-50 to-white p-8 shadow-lg">
          <h2 className="text-2xl font-bold text-slate-900">🚀 About BritMetrics</h2>
          <p className="mt-4 text-slate-600">
            BritMetrics uses real-time data from multiple sources to provide accurate campaign forecasting
            and audience insights for outdoor advertising across UK cities.
          </p>
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border border-blue-200 bg-blue-50 p-4">
              <div className="text-3xl font-black text-blue-600">10+</div>
              <div className="mt-1 text-sm font-semibold text-slate-700">Campaign Types</div>
            </div>
            <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4">
              <div className="text-3xl font-black text-emerald-600">20+</div>
              <div className="mt-1 text-sm font-semibold text-slate-700">UK Locations</div>
            </div>
            <div className="rounded-xl border border-purple-200 bg-purple-50 p-4">
              <div className="text-3xl font-black text-purple-600">24/7</div>
              <div className="mt-1 text-sm font-semibold text-slate-700">Real-Time Updates</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

