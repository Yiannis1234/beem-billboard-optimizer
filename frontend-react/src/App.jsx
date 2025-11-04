import { useMemo, useState } from 'react'
import SelectField from './components/SelectField'
import MetricCard from './components/MetricCard'
import SectionCard from './components/SectionCard'
import { campaigns, cities, mockPrediction } from './data/mockData'

const Hero = () => (
  <header className="space-y-6 rounded-3xl bg-white p-8 shadow-sm lg:p-12">
    <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div className="space-y-4">
        <div className="inline-flex items-center gap-3 rounded-full bg-blue-50 px-4 py-2 text-sm font-semibold text-blue-600">
          <span className="text-lg">📊</span>
          <span>BritMetrics — Billboard Intelligence</span>
        </div>
        <h1 className="text-3xl font-black text-slate-900 sm:text-4xl lg:text-5xl">
          Smarter Outdoor Campaign Planning
        </h1>
        <p className="max-w-2xl text-base text-slate-600 sm:text-lg">
          Compare UK cities, match real audiences to your brand, and get creative, weather-aware recommendations before you book your next billboard.
        </p>
      </div>
      <div className="rounded-2xl border border-blue-100 bg-blue-50/80 p-6 shadow-inner">
        <ul className="space-y-3 text-sm font-medium text-blue-900">
          <li>✅ Audience match scoring for 10+ campaign types</li>
          <li>✅ Live weather & traffic context for each area</li>
          <li>✅ ROI calculator + tactical recommendations</li>
        </ul>
      </div>
    </div>
  </header>
)

const formatNumber = (value) => new Intl.NumberFormat('en-GB').format(value)

function App() {
  const [selectedCampaignId, setSelectedCampaignId] = useState(campaigns[0].id)
  const [selectedCityId, setSelectedCityId] = useState(cities[0].id)

  const availableAreas = useMemo(() => {
    const city = cities.find((c) => c.id === selectedCityId)
    return city?.areas ?? []
  }, [selectedCityId])

  const [selectedAreaId, setSelectedAreaId] = useState(availableAreas[0]?.value ?? '')
  const [isLoading, setIsLoading] = useState(false)
  const [prediction, setPrediction] = useState(mockPrediction)

  const selectedCampaign = campaigns.find((c) => c.id === selectedCampaignId)
  const selectedArea = availableAreas.find((area) => area.value === selectedAreaId)

  // Ensure the area updates when the user changes city
  const handleCityChange = (cityId) => {
    setSelectedCityId(cityId)
    const city = cities.find((c) => c.id === cityId)
    const firstArea = city?.areas?.[0]?.value ?? ''
    setSelectedAreaId(firstArea)
  }

  const runAnalysis = async () => {
    setIsLoading(true)

    try {
      // TODO: Replace mockPrediction with real API response once the backend endpoints are exposed.
      await new Promise((resolve) => setTimeout(resolve, 800))
      setPrediction({ ...mockPrediction, refreshedAt: new Date().toISOString() })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 pb-16">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 px-4 py-8 lg:py-12">
        <Hero />

        <SectionCard
          title="Step 1 · Select Your Campaign"
          description="Choose a campaign type to tailor the insights and recommendations to your audience."
          actions={
            <button
              type="button"
              onClick={runAnalysis}
              disabled={isLoading}
              className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-600/30 transition hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-200 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isLoading ? 'Analysing…' : 'Run Analysis'}
            </button>
          }
        >
          <div className="grid gap-6 lg:grid-cols-[2fr,3fr] lg:items-start">
            <SelectField
              label="Campaign Type"
              value={selectedCampaignId}
              onChange={setSelectedCampaignId}
              options={campaigns.map((campaign) => ({ value: campaign.id, label: campaign.name }))}
              helperText="Personalised recommendations will adapt to this audience."
            />

            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
              <h3 className="text-lg font-semibold text-slate-900">Audience Highlights</h3>
              <p className="mt-2 text-sm text-slate-600">{selectedCampaign.summary}</p>
              <ul className="mt-4 grid gap-2 text-sm text-slate-700 sm:grid-cols-2">
                {selectedCampaign.highlights.map((highlight) => (
                  <li key={highlight} className="flex items-start gap-2">
                    <span className="mt-1 h-2 w-2 rounded-full bg-blue-500" />
                    <span>{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </SectionCard>

        <SectionCard
          title="Step 2 · Choose City & Area"
          description="Compare Manchester and London zones to discover where your campaign resonates best."
        >
          <div className="grid gap-6 lg:grid-cols-3">
            <SelectField
              label="City"
              value={selectedCityId}
              onChange={handleCityChange}
              options={cities.map((city) => ({ value: city.id, label: city.name }))}
            />
            <SelectField
              label="Area"
              value={selectedAreaId}
              onChange={setSelectedAreaId}
              options={availableAreas.map((area) => ({ value: area.value, label: area.label }))}
              helperText={selectedArea?.description}
            />
            <div className="rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-600 shadow-sm">
              <p className="font-semibold text-slate-900">Area Snapshot</p>
              <p className="mt-2">
                {selectedArea?.meta ?? 'Target area data will appear here once connected to the live API.'}
              </p>
            </div>
          </div>
        </SectionCard>

        <SectionCard
          title="Campaign Forecast"
          description="Key performance signals based on historical footfall, audience fit, and current conditions."
        >
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            <MetricCard
              label="Success Score"
              value={prediction.successScore}
              suffix="/100"
              helper={`Confidence level: ${prediction.successLevel}`}
              accent="blue"
            />
            <MetricCard
              label="Audience Match"
              value={`${prediction.audienceMatch}%`}
              helper="How closely the area matches your campaign demographic"
              accent="green"
            />
            <MetricCard
              label="Impressions / Hour"
              value={formatNumber(prediction.impressionsPerHour)}
              helper="Estimated unique views during campaign flight"
              accent="purple"
            />
            <MetricCard
              label="Weather Impact"
              value={`${prediction.weather.visibilityScore}`}
              helper={prediction.weather.summary}
              accent="orange"
            />
          </div>
        </SectionCard>

        <SectionCard
          title="Context & Recommendations"
          description="Real-world signals and tactical guidance to maximise ROI."
        >
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900">Key Reasons This Area Works</h3>
              <ul className="mt-4 space-y-3 text-sm text-slate-600">
                {prediction.keyReasons.map((reason) => (
                  <li key={reason} className="flex items-start gap-3">
                    <span className="mt-1 text-lg">✨</span>
                    <span>{reason}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900">Tactical Recommendations</h3>
              <ul className="mt-4 space-y-3 text-sm text-slate-600">
                {prediction.tactics.map((tip) => (
                  <li key={tip} className="flex items-start gap-3">
                    <span className="mt-1 text-lg">🎯</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-blue-50 p-6 text-blue-900 shadow-sm">
              <h3 className="text-lg font-semibold">Weather & Movement Signals</h3>
              <dl className="mt-4 grid gap-3 text-sm">
                <div className="flex justify-between border-b border-blue-100 pb-2">
                  <dt className="font-medium">Conditions</dt>
                  <dd>{prediction.weather.condition}</dd>
                </div>
                <div className="flex justify-between border-b border-blue-100 pb-2">
                  <dt className="font-medium">Visibility</dt>
                  <dd>{prediction.weather.visibility}</dd>
                </div>
                <div className="flex justify-between border-b border-blue-100 pb-2">
                  <dt className="font-medium">Traffic</dt>
                  <dd>{prediction.traffic.status}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="font-medium">Events Nearby</dt>
                  <dd>{prediction.events.length > 0 ? `${prediction.events.length} upcoming` : 'No major events detected'}</dd>
                </div>
              </dl>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900">Upcoming Events</h3>
              {prediction.events.length === 0 ? (
                <p className="mt-3 text-sm text-slate-600">Link Eventbrite to surface relevant footfall spikes.</p>
              ) : (
                <ul className="mt-4 space-y-4 text-sm text-slate-600">
                  {prediction.events.map((event) => (
                    <li key={event.name} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                      <p className="font-semibold text-slate-900">{event.name}</p>
                      <p className="mt-1 text-xs uppercase tracking-wide text-slate-500">{event.date}</p>
                      <p className="mt-2 text-sm">{event.venue}</p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </SectionCard>

        <footer className="rounded-3xl bg-slate-900 px-6 py-10 text-slate-100 lg:px-10">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-lg font-semibold">Ready to move beyond Streamlit?</p>
              <p className="mt-2 text-sm text-slate-300">
                This React front-end is wired for API integration. Once the REST endpoints are exposed, hook them up in <code>src/api</code> to serve live data to your clients.
              </p>
            </div>
            <a
              href="mailto:vamvak@outlook.com"
              className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-900 shadow-lg shadow-black/10 transition hover:-translate-y-0.5 hover:bg-slate-100"
            >
              📬 Contact BritMetrics
            </a>
          </div>
        </footer>
      </div>
    </div>
  )
}

export default App
