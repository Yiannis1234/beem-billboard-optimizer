import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import SelectField from '../components/SelectField'
import MetricCard from '../components/MetricCard'
import SectionCard from '../components/SectionCard'
import api from '../lib/api'

const formatNumber = (value) => {
  if (value === null || value === undefined) {
    return '--'
  }
  return new Intl.NumberFormat('en-GB').format(value)
}

export default function Home() {
  const [campaigns, setCampaigns] = useState([])
  const [cities, setCities] = useState([])
  const [selectedCampaignId, setSelectedCampaignId] = useState('')
  const [selectedCityId, setSelectedCityId] = useState('')
  const [selectedAreaId, setSelectedAreaId] = useState('')

  const [prediction, setPrediction] = useState(null)
  const [isBootstrapping, setIsBootstrapping] = useState(true)
  const [isLoadingPrediction, setIsLoadingPrediction] = useState(false)
  const [error, setError] = useState(null)

  const areas = useMemo(() => {
    return cities.find((c) => c.id === selectedCityId)?.areas ?? []
  }, [cities, selectedCityId])

  const selectedCampaign = campaigns.find((c) => c.id === selectedCampaignId) ?? null
  const selectedArea = areas.find((a) => a.id === selectedAreaId) ?? null

  useEffect(() => {
    ;(async () => {
      try {
        setIsBootstrapping(true)
        setError(null)

        const [campaignsData, citiesData] = await Promise.all([
          api.fetchCampaigns(),
          api.fetchCities(),
        ])

        setCampaigns(campaignsData.campaigns)
        const defaultCampaignId = campaignsData.defaultCampaignId ?? campaignsData.campaigns[0]?.id ?? ''
        setSelectedCampaignId(defaultCampaignId)

        setCities(citiesData.cities)
        const defaultCityId = citiesData.defaultCityId ?? citiesData.cities[0]?.id ?? ''
        setSelectedCityId(defaultCityId)

        const firstArea = citiesData.cities.find((c) => c.id === defaultCityId)?.areas?.[0]?.id
        setSelectedAreaId(firstArea ?? '')

        if (defaultCityId && firstArea) {
          const predictionResponse = await api.predict({
            cityId: defaultCityId,
            areaId: firstArea,
            campaignId: defaultCampaignId,
          })
          setPrediction(predictionResponse)
        }
      } catch (err) {
        setError(err.message || 'Failed to load campaign configuration.')
      } finally {
        setIsBootstrapping(false)
      }
    })()
  }, [])

  const handleCityChange = (cityId) => {
    setSelectedCityId(cityId)
    const firstArea = cities.find((c) => c.id === cityId)?.areas?.[0]?.id ?? ''
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
  const keyReasons = prediction?.keyReasons ?? []
  const tactics = prediction?.personalizedTips ?? []
  const weather = prediction?.weather ?? null
  const traffic = prediction?.traffic ?? null
  const places = prediction?.places ?? null

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pb-16">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 px-4 py-8 lg:py-12">
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
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-600 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-500/30 transition hover:from-blue-700 hover:to-cyan-700 focus:outline-none focus:ring-4 focus:ring-blue-200 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isLoadingPrediction ? '🔄 Analysing…' : '🚀 Run Analysis'}
            </button>
          }
        >
          <div className="grid gap-6 lg:grid-cols-[2fr,3fr] lg:items-start">
            <SelectField
              label="Campaign Type"
              value={selectedCampaignId}
              onChange={setSelectedCampaignId}
              options={campaigns.map((c) => ({ value: c.id, label: c.name }))}
              helperText="Personalised recommendations will adapt to this audience."
              disabled={isBootstrapping}
            />
            <div className="rounded-2xl border border-blue-200 bg-gradient-to-br from-blue-50 to-cyan-50 p-5">
              <h3 className="text-lg font-semibold text-slate-900">Audience Highlights</h3>
              <p className="mt-2 text-sm text-slate-600">
                {selectedCampaign?.summary ?? 'Select a campaign to view tailored highlights.'}
              </p>
              <ul className="mt-4 grid gap-2 text-sm text-slate-700 sm:grid-cols-2">
                {(selectedCampaign?.highlights ?? []).map((h) => (
                  <li key={h} className="flex items-start gap-2">
                    <span className="mt-1 h-2 w-2 rounded-full bg-blue-500"></span>
                    <span>{h}</span>
                  </li>
                ))}
                {selectedCampaign && (selectedCampaign.highlights ?? []).length === 0 ? (
                  <li className="text-slate-500">
                    Ideal factors: {selectedCampaign.idealFactors?.join(', ') ?? 'See backend data for more details.'}
                  </li>
                ) : null}
              </ul>
            </div>
          </div>
        </SectionCard>

        <SectionCard
          title="Step 2 · Choose Your Location"
          description="Compare Manchester and London zones to discover where your campaign resonates best."
        >
          <div className="grid gap-6 lg:grid-cols-3">
            <SelectField
              label="City"
              value={selectedCityId}
              onChange={handleCityChange}
              options={cities.map((c) => ({ value: c.id, label: c.name }))}
              disabled={isBootstrapping || cities.length === 0}
              placeholder={isBootstrapping ? 'Loading cities…' : 'Select a city'}
            />
            <SelectField
              label="Area"
              value={selectedAreaId}
              onChange={setSelectedAreaId}
              options={areas.map((a) => ({ value: a.id, label: a.name }))}
              helperText={selectedArea?.description}
              disabled={isBootstrapping || areas.length === 0}
              placeholder={isBootstrapping ? 'Loading areas…' : 'Select an area'}
            />
            <div className="rounded-2xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-teal-50 p-4 text-sm text-slate-600 shadow-sm">
              <p className="font-semibold text-slate-900">📍 Area Snapshot</p>
              {selectedArea ? (
                <ul className="mt-2 space-y-1 text-sm">
                  <li>👥 Footfall: {formatNumber(selectedArea.footfallDaily)}/day</li>
                  <li>🏙️ Population: {formatNumber(selectedArea.population)}</li>
                  <li className="text-xs text-slate-500">{selectedArea.meta}</li>
                </ul>
              ) : (
                <p className="mt-2 text-slate-500">Select a city and area to view details.</p>
              )}
            </div>
          </div>
        </SectionCard>

        <SectionCard
          title="📊 Campaign Forecast"
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
              helper={
                audienceMatch !== null
                  ? 'How closely the area matches your campaign demographic'
                  : 'Select a campaign to unlock audience match.'
              }
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
        </SectionCard>

        <SectionCard
          title="💡 Context & Recommendations"
          description="Real-world signals and tactical guidance to maximise ROI."
        >
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-amber-200 bg-gradient-to-br from-amber-50 to-orange-50 p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-amber-900">✨ Key Reasons This Area Works</h3>
              <ul className="mt-4 space-y-3 text-sm text-slate-700">
                {keyReasons.length > 0 ? (
                  keyReasons.map((r) => (
                    <li key={r} className="flex items-start gap-3">
                      <span className="mt-1 text-lg">✨</span>
                      <span>{r}</span>
                    </li>
                  ))
                ) : (
                  <li className="text-slate-500">Run the analysis to surface the top area drivers.</li>
                )}
              </ul>
            </div>
            <div className="rounded-2xl border border-violet-200 bg-gradient-to-br from-violet-50 to-purple-50 p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-violet-900">🎯 Tactical Recommendations</h3>
              <ul className="mt-4 space-y-3 text-sm text-slate-700">
                {tactics.length > 0 ? (
                  tactics.map((t) => (
                    <li key={t} className="flex items-start gap-3">
                      <span className="mt-1 text-lg">🎯</span>
                      <span>{t}</span>
                    </li>
                  ))
                ) : (
                  <li className="text-slate-500">Select a campaign and run the analysis to unlock personalised tactics.</li>
                )}
              </ul>
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-sky-200 bg-gradient-to-br from-sky-50 to-blue-50 p-6 text-sky-900 shadow-sm">
              <h3 className="text-lg font-semibold">🌤️ Weather & Movement</h3>
              {weather ? (
                <dl className="mt-4 grid gap-3 text-sm">
                  <div className="flex justify-between border-b border-sky-100 pb-2">
                    <dt className="font-medium">Conditions</dt>
                    <dd>{weather.condition}</dd>
                  </div>
                  <div className="flex justify-between border-b border-sky-100 pb-2">
                    <dt className="font-medium">Temperature</dt>
                    <dd>{weather.temperatureC}°C</dd>
                  </div>
                  <div className="flex justify-between border-b border-sky-100 pb-2">
                    <dt className="font-medium">Visibility</dt>
                    <dd>{weather.visibilityKm} km</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="font-medium">Wind</dt>
                    <dd>{weather.windKph} kph</dd>
                  </div>
                </dl>
              ) : (
                <p className="mt-3 text-sm text-sky-700">No weather data available</p>
              )}
            </div>
            <div className="rounded-2xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-teal-50 p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-emerald-900">📍 Places Popularity</h3>
              {places ? (
                <dl className="mt-4 grid gap-3 text-sm text-emerald-900">
                  <div className="flex justify-between border-b border-emerald-100 pb-2">
                    <dt className="font-medium">Top Place</dt>
                    <dd>{places.placeName}</dd>
                  </div>
                  <div className="flex justify-between border-b border-emerald-100 pb-2">
                    <dt className="font-medium">Rating</dt>
                    <dd>⭐ {places.rating} ({places.userRatingsTotal} reviews)</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="font-medium">Popularity Score</dt>
                    <dd>{places.popularityScore}/100</dd>
                  </div>
                </dl>
              ) : (
                <p className="mt-3 text-sm text-emerald-700">No place data available</p>
              )}
            </div>
          </div>
        </SectionCard>

        <div className="flex items-center justify-center gap-4">
          <Link
            to="/analytics"
            className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-purple-500/30 transition hover:from-purple-700 hover:to-pink-700"
          >
            📈 View Analytics Dashboard
          </Link>
        </div>
      </div>
    </div>
  )
}

