import { useEffect, useMemo, useState } from 'react'
import SelectField from './components/SelectField'
import MetricCard from './components/MetricCard'
import SectionCard from './components/SectionCard'
import api from './lib/api'

const Hero = () => (
  <header className="space-y-6 rounded-3xl bg-gradient-to-br from-blue-600 to-blue-700 p-8 shadow-xl lg:p-12">
    <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
      <div className="space-y-4">
        <div className="inline-flex items-center gap-4 rounded-2xl bg-white/10 px-6 py-3 backdrop-blur-sm">
          <svg className="h-10 w-10" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="40" height="40" rx="8" fill="white" fillOpacity="0.2"/>
            <path d="M20 10L28 16V26L20 32L12 26V16L20 10Z" fill="white"/>
            <path d="M20 15L24 18V24L20 27L16 24V18L20 15Z" fill="#0078FF"/>
          </svg>
          <span className="text-2xl font-black tracking-tight text-white">
            BritMetrics
          </span>
        </div>
        <h1 className="text-3xl font-black text-white sm:text-4xl lg:text-5xl">
          Smarter Outdoor Campaign Planning
        </h1>
        <p className="max-w-2xl text-base text-blue-100 sm:text-lg">
          Compare UK cities, match real audiences to your brand, and get creative, weather-aware recommendations before you book your next billboard.
        </p>
      </div>
      <div className="rounded-2xl border border-white/20 bg-white/10 p-6 shadow-inner backdrop-blur-sm">
        <ul className="space-y-3 text-sm font-medium text-white">
          <li>✅ Audience match scoring for 10+ campaign types</li>
          <li>✅ Live weather & traffic context for each area</li>
          <li>✅ ROI calculator + tactical recommendations</li>
        </ul>
      </div>
    </div>
  </header>
)

const formatNumber = (value) => {
  if (value === null || value === undefined) {
    return '--'
  }
  return new Intl.NumberFormat('en-GB').format(value)
}

function App() {
  const [campaigns, setCampaigns] = useState([])
  const [cities, setCities] = useState([])
  const [selectedCampaignId, setSelectedCampaignId] = useState('')
  const [selectedCityId, setSelectedCityId] = useState('')
  const [selectedAreaId, setSelectedAreaId] = useState('')

  const [prediction, setPrediction] = useState(null)
  const [isBootstrapping, setIsBootstrapping] = useState(true)
  const [isLoadingPrediction, setIsLoadingPrediction] = useState(false)
  const [error, setError] = useState(null)

  const availableAreas = useMemo(() => {
    const city = cities.find((c) => c.id === selectedCityId)
    return city?.areas ?? []
  }, [cities, selectedCityId])

  const selectedCampaign = campaigns.find((campaign) => campaign.id === selectedCampaignId) ?? null
  const selectedArea = availableAreas.find((area) => area.id === selectedAreaId) ?? null

  useEffect(() => {
    const bootstrap = async () => {
      try {
        setIsBootstrapping(true)
        setError(null)
        const [campaignResponse, cityResponse] = await Promise.all([api.fetchCampaigns(), api.fetchCities()])

        setCampaigns(campaignResponse.campaigns)
        const defaultCampaignId = campaignResponse.defaultCampaignId ?? campaignResponse.campaigns[0]?.id ?? ''
        setSelectedCampaignId(defaultCampaignId)

        setCities(cityResponse.cities)
        const defaultCityId = cityResponse.defaultCityId ?? cityResponse.cities[0]?.id ?? ''
        setSelectedCityId(defaultCityId)

        const defaultAreaId = cityResponse.cities
          .find((city) => city.id === defaultCityId)
          ?.areas?.[0]?.id

        setSelectedAreaId(defaultAreaId ?? '')

        if (defaultCityId && defaultAreaId) {
          const predictionResponse = await api.predict({
            cityId: defaultCityId,
            areaId: defaultAreaId,
            campaignId: defaultCampaignId,
          })
          setPrediction(predictionResponse)
        }
      } catch (err) {
        setError(err.message || 'Failed to load campaign configuration.')
      } finally {
        setIsBootstrapping(false)
      }
    }

    bootstrap()
  }, [])

  const handleCityChange = (cityId) => {
    setSelectedCityId(cityId)
    const city = cities.find((c) => c.id === cityId)
    const firstArea = city?.areas?.[0]?.id ?? ''
    setSelectedAreaId(firstArea)
  }

  const runAnalysis = async () => {
    if (!selectedCityId || !selectedAreaId) {
      setError('Select a city and area before running the analysis.')
      return
    }

    setIsLoadingPrediction(true)
    setError(null)

    try {
      const predictionResponse = await api.predict({
        cityId: selectedCityId,
        areaId: selectedAreaId,
        campaignId: selectedCampaignId,
      })
      setPrediction(predictionResponse)
    } catch (err) {
      setError(err.message || 'Failed to fetch prediction. Check the API server logs.')
    } finally {
      setIsLoadingPrediction(false)
    }
  }

  const audienceMatch = prediction?.audienceMatch ?? null
  const events = prediction?.events ?? []
  const keyReasons = prediction?.keyReasons ?? []
  const tactics = prediction?.personalizedTips ?? []
  const weather = prediction?.weather ?? null
  const traffic = prediction?.traffic ?? null
  const places = prediction?.places ?? null
  const lastUpdated = prediction?.refreshedAt ? new Date(prediction.refreshedAt) : null

  return (
    <div className="min-h-screen bg-slate-100 pb-16">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 px-4 py-8 lg:py-12">
        <Hero />

        {error ? (
          <div className="rounded-3xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 shadow-sm">
            {error}
          </div>
        ) : null}

        <SectionCard
          title="Step 1 · Select Your Campaign"
          description="Choose a campaign type to tailor the insights and recommendations to your audience."
          actions={
            <button
              type="button"
              onClick={runAnalysis}
              disabled={isBootstrapping || isLoadingPrediction}
              className="inline-flex items-center gap-2 rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-600/30 transition hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-200 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isLoadingPrediction ? 'Analysing…' : 'Run Analysis'}
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
              disabled={isBootstrapping}
            />

            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
              <h3 className="text-lg font-semibold text-slate-900">Audience Highlights</h3>
              <p className="mt-2 text-sm text-slate-600">{selectedCampaign?.summary ?? 'Select a campaign to view tailored highlights.'}</p>
              <ul className="mt-4 grid gap-2 text-sm text-slate-700 sm:grid-cols-2">
                {(selectedCampaign?.highlights ?? []).map((highlight) => (
                  <li key={highlight} className="flex items-start gap-2">
                    <span className="mt-1 h-2 w-2 rounded-full bg-blue-500" />
                    <span>{highlight}</span>
                  </li>
                ))}
                {selectedCampaign && (selectedCampaign.highlights ?? []).length === 0 ? (
                  <li className="text-slate-500">Ideal factors: {selectedCampaign.idealFactors?.join(', ') ?? 'See backend data for more details.'}</li>
                ) : null}
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
              disabled={isBootstrapping || cities.length === 0}
              placeholder={isBootstrapping ? 'Loading cities…' : 'Select a city'}
            />
            <SelectField
              label="Area"
              value={selectedAreaId}
              onChange={setSelectedAreaId}
              options={availableAreas.map((area) => ({ value: area.id, label: area.name }))}
              helperText={selectedArea?.description}
              disabled={isBootstrapping || availableAreas.length === 0}
              placeholder={isBootstrapping ? 'Loading areas…' : 'Select an area'}
            />
            <div className="rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-600 shadow-sm">
              <p className="font-semibold text-slate-900">Area Snapshot</p>
              {selectedArea ? (
                <ul className="mt-2 space-y-1 text-sm">
                  <li>Footfall daily: {formatNumber(selectedArea.footfallDaily)}</li>
                  <li>Population: {formatNumber(selectedArea.population)}</li>
                  <li>{selectedArea.meta}</li>
                </ul>
              ) : (
                <p className="mt-2 text-slate-500">Select a city and area to view details.</p>
              )}
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
              value={prediction?.successScore ?? '--'}
              suffix="/100"
              helper={prediction?.successLevel ?? 'Run the analysis to calculate the score.'}
              accent="blue"
            />
            <MetricCard
              label="Audience Match"
              value={audienceMatch ?? '--'}
              suffix={audienceMatch !== null ? '%' : ''}
              helper={audienceMatch !== null ? 'How closely the area matches your campaign demographic' : 'Select a campaign to unlock audience match.'}
              accent="green"
            />
            <MetricCard
              label="Impressions / Hour"
              value={formatNumber(prediction?.impressionsPerHour)}
              helper="Estimated unique views during campaign flight"
              accent="purple"
            />
            <MetricCard
              label="Target Audience / Hour"
              value={formatNumber(prediction?.targetAudienceSize)}
              helper="Expected reach among your core audience"
              accent="orange"
            />
          </div>
          {lastUpdated ? (
            <p className="text-right text-xs text-slate-500">Last refreshed {lastUpdated.toLocaleString()}</p>
          ) : null}
        </SectionCard>

        <SectionCard
          title="Context & Recommendations"
          description="Real-world signals and tactical guidance to maximise ROI."
        >
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900">Key Reasons This Area Works</h3>
              <ul className="mt-4 space-y-3 text-sm text-slate-600">
                {keyReasons.length > 0
                  ? keyReasons.map((reason) => (
                      <li key={reason} className="flex items-start gap-3">
                        <span className="mt-1 text-lg">✨</span>
                        <span>{reason}</span>
                      </li>
                    ))
                  : (
                      <li className="text-slate-500">Run the analysis to surface the top area drivers.</li>
                    )}
              </ul>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900">Tactical Recommendations</h3>
              <ul className="mt-4 space-y-3 text-sm text-slate-600">
                {tactics.length > 0
                  ? tactics.map((tip) => (
                      <li key={tip} className="flex items-start gap-3">
                        <span className="mt-1 text-lg">🎯</span>
                        <span>{tip}</span>
                      </li>
                    ))
                  : (
                      <li className="text-slate-500">Select a campaign and run the analysis to unlock personalised tactics.</li>
                    )}
              </ul>
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-blue-50 p-6 text-blue-900 shadow-sm">
              <h3 className="text-lg font-semibold">Weather & Movement Signals</h3>
              {weather ? (
                <dl className="mt-4 grid gap-3 text-sm">
                  <div className="flex justify-between border-b border-blue-100 pb-2">
                    <dt className="font-medium">Conditions</dt>
                    <dd>{weather.condition}</dd>
                  </div>
                  <div className="flex justify-between border-b border-blue-100 pb-2">
                    <dt className="font-medium">Temperature</dt>
                    <dd>{weather.temperatureC}°C</dd>
                  </div>
                  <div className="flex justify-between border-b border-blue-100 pb-2">
                    <dt className="font-medium">Visibility</dt>
                    <dd>{weather.visibilityKm} km</dd>
                  </div>
                  <div className="flex justify-between border-b border-blue-100 pb-2">
                    <dt className="font-medium">Wind</dt>
                    <dd>{weather.windKph} kph</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="font-medium">Precipitation</dt>
                    <dd>{weather.precipMm} mm</dd>
                  </div>
                </dl>
              ) : (
                <p className="mt-3 text-sm text-blue-800">Weather API data not available – check credentials.</p>
              )}
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900">Upcoming Events</h3>
              {events.length === 0 ? (
                <p className="mt-3 text-sm text-slate-600">Link Eventbrite to surface relevant footfall spikes.</p>
              ) : (
                <ul className="mt-4 space-y-4 text-sm text-slate-600">
                  {events.map((event) => (
                    <li key={event.id} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                      <p className="font-semibold text-slate-900">{event.name}</p>
                      <p className="mt-1 text-xs uppercase tracking-wide text-slate-500">{event.start}</p>
                      <p className="mt-2 text-sm">{event.venue}</p>
                      {event.url ? (
                        <a
                          href={event.url}
                          target="_blank"
                          rel="noreferrer"
                          className="mt-2 inline-flex items-center text-xs font-semibold text-blue-600 hover:text-blue-700"
                        >
                          View event →
                        </a>
                      ) : null}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900">Traffic Snapshot</h3>
              {traffic ? (
                <ul className="mt-3 space-y-2 text-sm text-slate-600">
                  <li>Congestion: {traffic.congestionLevel}</li>
                  <li>Current speed: {traffic.currentSpeed} km/h (free flow {traffic.freeFlowSpeed} km/h)</li>
                  <li>Delay: {traffic.delayMinutes} minutes</li>
                  <li>Data source: {traffic.apiStatus}</li>
                </ul>
              ) : (
                <p className="mt-3 text-sm text-slate-600">Traffic data unavailable.</p>
              )}
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-slate-900">Places Popularity</h3>
              {places ? (
                <ul className="mt-3 space-y-2 text-sm text-slate-600">
                  <li>Top place: {places.placeName}</li>
                  <li>Rating: {places.rating} ({formatNumber(places.userRatingsTotal)} reviews)</li>
                  <li>Popularity score: {places.popularityScore}/100</li>
                  <li>Data source: {places.apiStatus}</li>
                </ul>
              ) : (
                <p className="mt-3 text-sm text-slate-600">Connect Google Places API to view local venue popularity.</p>
              )}
            </div>
          </div>
        </SectionCard>

        <footer className="rounded-3xl bg-slate-900 px-6 py-10 text-slate-100 lg:px-10">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-lg font-semibold">React Front-end · API powered</p>
              <p className="mt-2 text-sm text-slate-300">
                The UI now consumes live BritMetrics API endpoints. Run <code>uvicorn backend.api_server:app --reload</code> and <code>npm run dev</code> to work locally.
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
