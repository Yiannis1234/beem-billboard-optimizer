export default function Analytics() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-orange-50 pb-12 sm:pb-16">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-3 py-6 sm:gap-8 sm:px-4 sm:py-8 lg:py-12">
        {/* Header */}
        <div className="flex items-center justify-between rounded-2xl bg-gradient-to-r from-purple-600 to-pink-600 p-4 shadow-xl sm:rounded-3xl sm:p-8">
          <div>
            <h1 className="text-2xl font-black text-white sm:text-3xl lg:text-4xl">Analytics Dashboard</h1>
            <p className="mt-2 text-sm text-purple-100 sm:text-base lg:text-lg">Deep insights into your campaign performance and audience reach</p>
          </div>
          <div className="hidden lg:block">
            <svg className="h-24 w-24" viewBox="0 0 100 100" fill="none">
              <circle cx="50" cy="50" r="45" fill="white" fillOpacity="0.2" />
              <path d="M30 70L40 50L50 60L60 40L70 55L80 30" stroke="white" strokeWidth="4" strokeLinecap="round" />
            </svg>
          </div>
        </div>

        {/* Info Message */}
        <div className="rounded-2xl border border-amber-200 bg-gradient-to-br from-amber-50 to-orange-50 p-4 shadow-lg sm:rounded-3xl sm:p-6">
          <h2 className="text-lg font-bold text-amber-900 sm:text-xl">📊 Analytics Dashboard</h2>
          <p className="mt-2 text-xs font-medium text-amber-900 sm:text-sm">
            This dashboard will display real campaign analytics once you run analyses on the Campaign Planner page.
            All data shown here will be based on actual predictions and results from your campaign analyses.
          </p>
          <div className="mt-4 rounded-xl border border-amber-200 bg-white p-3 sm:p-4">
            <p className="text-xs font-semibold text-slate-900 sm:text-sm">To view analytics:</p>
            <ol className="mt-2 list-decimal list-inside space-y-1 text-xs font-medium text-slate-800 sm:text-sm">
              <li>Go to the Campaign Planner page</li>
              <li>Select a campaign type, city, and area</li>
              <li>Run the analysis to generate real data</li>
              <li>Return here to see aggregated insights (coming soon)</li>
            </ol>
          </div>
        </div>

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

