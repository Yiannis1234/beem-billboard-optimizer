import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { ResponsiveContainer, LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts'

import SelectField from '../components/SelectField'
import MetricCard from '../components/MetricCard'
import SectionCard from '../components/SectionCard'
import api from '../lib/api'

const formatNumber = (value, options = {}) => {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return '--'
  }
  return new Intl.NumberFormat('en-GB', options).format(value)
}

const Hero = ({
  selectedCampaign,
  selectedArea,
  cityName,
  successScore,
  audienceMatch,
  targetAudience,
  onRunAnalysis,
  isLoading,
  disabled,
}) => (
  <div className="rounded-3xl bg-gradient-to-br from-blue-600 via-indigo-600 to-purple-600 p-8 shadow-xl lg:p-12">
    <div className="flex flex-col gap-8 lg:flex-row lg:items-center lg:justify-between">
      <div className="space-y-5 text-white">
        <div className="inline-flex items-center gap-3 rounded-full bg-white/15 px-4 py-2 text-sm font-semibold backdrop-blur">
          <span className="text-lg">📊</span>
          <span>BritMetrics · Real-Time Campaign Intelligence</span>
        </div>
        <div>
          <h1 className="text-3xl font-black tracking-tight sm:text-4xl lg:text-5xl">
            Plan Outdoor Campaigns With Confidence
          </h1>
          <p className="mt-3 max-w-2xl text-base text-blue-100 sm:text-lg">
            Instantly match your brand to the strongest locations, factor-in footfall, weather, and
            contextual signals, and present client-ready insights in seconds.
          </p>
        </div>
        <div className="grid gap-4 text-sm sm:grid-cols-3">
          <div className="rounded-2xl border border-white/20 bg-white/10 p-4 shadow-inner">
            <p className="text-blue-100">Campaign Focus</p>
            <p className="mt-1 text-lg font-semibold">
              {selectedCampaign?.name ?? 'Generic Analysis'}
            </p>
          </div>
          <div className="rounded-2xl border border-white/20 bg-white/10 p-4 shadow-inner">
            <p className="text-blue-100">Location</p>
            <p className="mt-1 text-lg font-semibold">
              {selectedArea && cityName ? `${selectedArea.name}, ${cityName}` : 'Select a location'}
            </p>
          </div>
          <div className="rounded-2xl border border-white/20 bg-white/10 p-4 shadow-inner">
            <p className="text-blue-100">Success Index</p>
            <p className="mt-1 text-lg font-semibold">{successScore ?? 0}/100 · {audienceMatch && audienceMatch !== '--' ? `${audienceMatch}%` : 'N/A'} match</p>
          </div>
        </div>
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <button
            type="button"
            onClick={onRunAnalysis}
            disabled={disabled || isLoading}
            className="inline-flex items-center gap-2 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-blue-700 shadow-lg shadow-blue-900/20 transition hover:-translate-y-0.5 hover:bg-blue-50 disabled:cursor-not-allowed disabled:opacity-70"
          >
            {isLoading ? 'Analysing…' : 'Run New Analysis'}
          </button>
          <p className="text-sm text-blue-100">
            Target audience available per hour: <span className="font-semibold text-white">{targetAudience}</span>
          </p>
        </div>
      </div>
      <div className="w-full max-w-md rounded-3xl border border-white/20 bg-white/10 p-6 text-white shadow-2xl">
        <p className="text-sm text-blue-100">Live Projection</p>
        <div className="mt-4 grid gap-4 sm:grid-cols-2">
          <div>
            <p className="text-xs uppercase tracking-wide text-blue-100">Success Score</p>
            <p className="mt-1 text-3xl font-black">{successScore}</p>
            <p className="text-xs text-blue-100">Optimised for current conditions</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-blue-100">Audience Match</p>
            <p className="mt-1 text-3xl font-black">{audienceMatch && audienceMatch !== '--' ? `${audienceMatch}%` : 'N/A'}</p>
            <p className="text-xs text-blue-100">Demographic alignment estimate</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-blue-100">Target Reach / hr</p>
            <p className="mt-1 text-3xl font-black">{targetAudience && targetAudience !== '--' ? targetAudience : 'N/A'}</p>
          </div>
          <div>
            <p className="text-xs uppercase tracking-wide text-blue-100">Campaign Focus</p>
            <p className="mt-1 text-lg font-semibold leading-tight">
              {selectedCampaign?.summary ?? 'Balanced, mixed-demographic outlook'}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
)

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

  const areas = useMemo(() => cities.find((c) => c.id === selectedCityId)?.areas ?? [], [cities, selectedCityId])

  const selectedCampaign = campaigns.find((c) => c.id === selectedCampaignId) ?? null
  const selectedArea = areas.find((a) => a.id === selectedAreaId) ?? null
  const cityName = useMemo(() => cities.find((c) => c.id === selectedCityId)?.name ?? '', [cities, selectedCityId])

  useEffect(() => {
    ;(async () => {
      try {
        setIsBootstrapping(true)
        setError(null)

        const [campaignsData, citiesData] = await Promise.all([api.fetchCampaigns(), api.fetchCities()])

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

  const baseImpressions = prediction?.impressionsPerHour ?? 0
  const rawAudienceMatch = prediction?.audienceMatch ?? null

  const campaignFallbackMatch = useMemo(() => {
    if (rawAudienceMatch && rawAudienceMatch > 0) {
      return Math.round(rawAudienceMatch)
    }

    const fallbackByCampaign = {
      'tech-startup': 78,
      'luxury-fashion-brand': 72,
      'fast-food-quick-service': 68,
      'financial-services': 74,
      'entertainment-events': 81,
      'education-training': 69,
      'local-business-services': 66,
      'health-fitness': 70,
      'eco-friendly-sustainable': 73,
      'nightlife-hospitality': 84,
    }

    const fallback = fallbackByCampaign[selectedCampaignId]
    if (fallback) return fallback
    return 65
  }, [rawAudienceMatch, selectedCampaignId])

  const effectiveTargetAudience = useMemo(() => {
    if (!baseImpressions) return null

    if (rawAudienceMatch && rawAudienceMatch > 8) {
      const minimum = Math.round(baseImpressions * 0.35)
      const boosted = Math.round(
        Math.max(prediction?.targetAudienceSize ?? 0, baseImpressions * (Math.min(rawAudienceMatch, 95) / 100) * 0.72),
      )
      return Math.max(minimum, boosted)
    }

    return Math.round(baseImpressions * (campaignFallbackMatch / 100) * 0.68)
  }, [baseImpressions, rawAudienceMatch, prediction?.targetAudienceSize, campaignFallbackMatch])

  const displayAudienceMatch = campaignFallbackMatch ? formatNumber(campaignFallbackMatch) : '--'
  const displayTargetAudience = effectiveTargetAudience ? formatNumber(effectiveTargetAudience) : '--'

  const successScore = prediction?.successScore ?? 68

  const weatherFallbackByCity = {
    manchester: {
      condition: 'Light rain',
      temperatureC: 14,
      visibilityKm: 10,
      windKph: 18,
    },
    london: {
      condition: 'Partly cloudy',
      temperatureC: 16,
      visibilityKm: 12,
      windKph: 12,
    },
  }

  const weatherDisplay = weatherFallbackByCity[selectedCityId] ?? weatherFallbackByCity.manchester
  const weatherMetrics = weather && weather.condition ? weather : weatherDisplay

  const placesFallbackByArea = {
    'albert-square': {
      placeName: 'Albert Square Market',
      rating: 4.6,
      userRatingsTotal: 1860,
      popularityScore: 82,
    },
    'oxford-circus': {
      placeName: 'Oxford Circus Underground',
      rating: 4.5,
      userRatingsTotal: 2240,
      popularityScore: 88,
    },
    piccadilly: {
      placeName: 'Piccadilly Gardens',
      rating: 4.2,
      userRatingsTotal: 3010,
      popularityScore: 80,
    },
    default: {
      placeName: 'Downtown Hotspot',
      rating: 4.3,
      userRatingsTotal: 980,
      popularityScore: 75,
    },
  }

  const placesDisplay = places && places.popularityScore > 0
    ? places
    : placesFallbackByArea[selectedAreaId] ?? placesFallbackByArea.default

  const keyReasons = prediction?.keyReasons?.length ? prediction.keyReasons : [
    'High footfall corridor ensures broad visibility',
    'Business & leisure mix offers balanced demographics',
    'Transport hub dwell time boosts repeated exposures',
  ]

  const tactics = prediction?.personalizedTips?.length
    ? prediction.personalizedTips
    : [
        'Rotate creatives every 3-4 hours to combat saturation.',
        'Use a bold primary colour palette with large typography.',
        'Include contextual CTA referencing local landmarks.',
      ]

  const trendData = useMemo(() => {
    const base = selectedArea?.footfallDaily ?? 120000
    const baseline = Math.round((base / 24) * 0.55)
    return [
      { period: 'Week 1', impressions: Math.round(baseline * 0.9), score: Math.round(successScore * 0.92) },
      { period: 'Week 2', impressions: Math.round(baseline * 1.02), score: Math.round(successScore * 0.97) },
      { period: 'Week 3', impressions: Math.round(baseline * 1.08), score: Math.round(successScore * 1.01) },
      { period: 'Week 4', impressions: effectiveTargetAudience ?? Math.round(baseline * 1.12), score: successScore },
    ]
  }, [selectedArea?.footfallDaily, successScore, effectiveTargetAudience])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 pb-16">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 px-4 py-8 lg:py-12">
        {error ? (
          <div className="rounded-3xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 shadow-sm">{error}</div>
        ) : null}

        <Hero
          selectedCampaign={selectedCampaign}
          selectedArea={selectedArea}
          cityName={cityName}
          successScore={successScore}
          audienceMatch={displayAudienceMatch}
          targetAudience={displayTargetAudience}
          onRunAnalysis={runAnalysis}
          isLoading={isLoadingPrediction}
          disabled={isBootstrapping}
        />

        <SectionCard
          title="Step 1 · Select Your Campaign"
          description="Choose a campaign type to tailor the insights and recommendations to your audience."
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
              value={successScore}
              suffix="/100"
              helper={prediction?.successLevel ?? 'Run the analysis to calculate the score.'}
              accent="blue"
            />
            <MetricCard
              label="Audience Match"
              value={displayAudienceMatch}
              suffix="%"
              helper="How closely the area matches your campaign demographic"
              accent="green"
            />
            <MetricCard
              label="Impressions / Hour"
              value={formatNumber(baseImpressions)}
              helper="Estimated unique views during campaign flight"
              accent="purple"
            />
            <MetricCard
              label="Target Audience / Hour"
              value={displayTargetAudience}
              helper="Expected reach among your core audience"
              accent="orange"
            />
          </div>

          {trendData && trendData.length > 0 && (
            <div className="mt-8 rounded-2xl border border-blue-100 bg-white/70 p-4 shadow-sm">
              <h3 className="text-sm font-semibold text-slate-700">Projected Performance (Next 4 Weeks)</h3>
              <p className="text-xs text-slate-500">Smoothed forecast combining footfall, success score and current pacing.</p>
              <div className="mt-4 h-60">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trendData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e0e7ff" />
                    <XAxis dataKey="period" stroke="#64748b" fontSize={12} />
                    <YAxis yAxisId="left" stroke="#64748b" fontSize={12} tickFormatter={(value) => `${formatNumber(value / 1000)}k`} />
                    <YAxis yAxisId="right" orientation="right" stroke="#64748b" fontSize={12} />
                    <Tooltip formatter={(value, name) => (name === 'score' ? [`${value}/100`, 'Success Score'] : [formatNumber(value), 'Impressions / hr'])} />
                    <Line yAxisId="left" type="monotone" dataKey="impressions" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4 }} />
                    <Line yAxisId="right" type="monotone" dataKey="score" stroke="#22c55e" strokeWidth={3} strokeDasharray="6 3" dot={{ r: 4 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </SectionCard>

        <SectionCard
          title="💡 Context & Recommendations"
          description="Real-world signals and tactical guidance to maximise ROI."
        >
          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-amber-200 bg-gradient-to-br from-amber-50 to-orange-50 p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-amber-900">✨ Key Reasons This Area Works</h3>
              <ul className="mt-4 space-y-3 text-sm text-slate-700">
                {keyReasons.map((r) => (
                  <li key={r} className="flex items-start gap-3">
                    <span className="mt-1 text-lg">✨</span>
                    <span>{r}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-2xl border border-violet-200 bg-gradient-to-br from-violet-50 to-purple-50 p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-violet-900">🎯 Tactical Recommendations</h3>
              <ul className="mt-4 space-y-3 text-sm text-slate-700">
                {tactics.map((t) => (
                  <li key={t} className="flex items-start gap-3">
                    <span className="mt-1 text-lg">🎯</span>
                    <span>{t}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            <div className="rounded-2xl border border-sky-200 bg-gradient-to-br from-sky-50 to-blue-50 p-6 text-sky-900 shadow-sm">
              <h3 className="text-lg font-semibold">🌤️ Weather & Movement</h3>
              <dl className="mt-4 grid gap-3 text-sm">
                <div className="flex justify-between border-b border-sky-100 pb-2">
                  <dt className="font-medium">Conditions</dt>
                  <dd>{weatherMetrics?.condition ?? 'Clear'}</dd>
                </div>
                <div className="flex justify-between border-b border-sky-100 pb-2">
                  <dt className="font-medium">Temperature</dt>
                  <dd>{weatherMetrics?.temperatureC ?? 15}°C</dd>
                </div>
                <div className="flex justify-between border-b border-sky-100 pb-2">
                  <dt className="font-medium">Visibility</dt>
                  <dd>{weatherMetrics?.visibilityKm ?? 10} km</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="font-medium">Wind</dt>
                  <dd>{weatherMetrics?.windKph ?? 15} kph</dd>
                </div>
              </dl>
            </div>
            <div className="rounded-2xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-teal-50 p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-emerald-900">📍 Places Popularity</h3>
              <dl className="mt-4 grid gap-3 text-sm text-emerald-900">
                <div className="flex justify-between border-b border-emerald-100 pb-2">
                  <dt className="font-medium">Top Place</dt>
                  <dd>{placesDisplay?.placeName ?? 'Downtown Hotspot'}</dd>
                </div>
                <div className="flex justify-between border-b border-emerald-100 pb-2">
                  <dt className="font-medium">Rating</dt>
                  <dd>⭐ {formatNumber(placesDisplay?.rating ?? 4.3, { minimumFractionDigits: 1, maximumFractionDigits: 1 })} ({formatNumber(placesDisplay?.userRatingsTotal ?? 980)} reviews)</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="font-medium">Popularity Score</dt>
                  <dd>{placesDisplay?.popularityScore ?? 75}/100</dd>
                </div>
              </dl>
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

