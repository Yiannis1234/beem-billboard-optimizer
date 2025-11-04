export const campaigns = [
  {
    id: 'none',
    name: 'None (Generic Analysis)',
    summary: 'Generic analysis is great for quick comparisons. Connect to the API to unlock live audience match data.',
    highlights: [
      'See base footfall and success scores for any area',
      'Understand how weather and traffic alter visibility',
      'Share quick insights with clients even before onboarding',
    ],
  },
  {
    id: 'luxury-fashion',
    name: 'Luxury Fashion Brand',
    summary: 'Affluent shoppers, premium retail environments, and high dwell-time transit hubs are the core focus.',
    highlights: [
      'Affluent audiences in business districts',
      'High-end shopping behaviour + brand conscious crowd',
      'Premium creative slots with extended visibility',
    ],
  },
  {
    id: 'tech-startup',
    name: 'Tech Startup',
    summary: 'Young professionals, students, and forward-thinking commuters with high mobile engagement.',
    highlights: [
      'University and innovation districts',
      'High QR-scan propensity and social sharing',
      'Great for app installs and beta launches',
    ],
  },
  {
    id: 'fast-food',
    name: 'Fast Food / Quick Service',
    summary: 'Commuters, students, and leisure shoppers with high impulse purchase behaviour.',
    highlights: [
      'Transport hubs with morning + evening spikes',
      'High dwell around shopping districts',
      'Weather reactive messaging for seasonal menus',
    ],
  },
]

export const cities = [
  {
    id: 'manchester',
    name: 'Manchester',
    areas: [
      {
        value: 'Albert Square',
        label: 'Albert Square',
        description: 'Historic square next to the Town Hall with strong footfall and professional audiences.',
        meta: 'Avg footfall: 120k/day · Success: Premium retail + civic events',
      },
      {
        value: 'Oxford Road',
        label: 'Oxford Road',
        description: 'University corridor with heavy student and young professional audience.',
        meta: 'High student density · Nighttime leisure traffic',
      },
      {
        value: 'Spinningfields',
        label: 'Spinningfields',
        description: 'Financial district with affluent professionals and evening hospitality crowd.',
        meta: 'Premium finance + hospitality audience mix',
      },
      {
        value: 'Northern Quarter',
        label: 'Northern Quarter',
        description: 'Creative and nightlife district ideal for trend-led campaigns.',
        meta: 'Creative industries · High social sharing',
      },
      {
        value: 'MediaCityUK',
        label: 'MediaCityUK',
        description: 'Broadcast and tech hub with daytime professionals and event visitors.',
        meta: 'Media workforce · Event-led spikes',
      },
    ],
  },
  {
    id: 'london',
    name: 'London',
    areas: [
      {
        value: 'Oxford Circus',
        label: 'Oxford Circus',
        description: 'West End shopping epicentre with global retail brands and tourist flow.',
        meta: 'Footfall 400k/day · Luxury + mainstream retail',
      },
      {
        value: 'Kings Cross',
        label: "King's Cross",
        description: 'Major rail hub with international travellers and office workers.',
        meta: 'Commuter dominance · Long dwell platforms',
      },
      {
        value: 'Shoreditch',
        label: 'Shoreditch',
        description: 'Creative hub for startups, nightlife, and experiential activations.',
        meta: 'Tech + nightlife blend · Street culture',
      },
      {
        value: 'Canary Wharf',
        label: 'Canary Wharf',
        description: 'Financial powerhouse with ultra-affluent professionals and corporate HQs.',
        meta: 'Finance-first audience · High CPM slots',
      },
      {
        value: 'Camden Town',
        label: 'Camden Town',
        description: 'Music, markets, and alternative culture with strong weekend footfall.',
        meta: 'Youth + tourist heavy · Night economy',
      },
    ],
  },
]

export const mockPrediction = {
  successScore: 84,
  successLevel: 'Excellent Fit',
  audienceMatch: 76,
  impressionsPerHour: 1825,
  keyReasons: [
    'High dwell time from commuter queues and pedestrian crossings',
    'Affluent professionals align with premium pricing strategy',
    'Weather is clear with great visibility on digital panels',
  ],
  tactics: [
    'Rotate creative by daypart to target morning commuters vs. evening shoppers',
    'Add QR codes that trigger incentives aligned with current weather',
    'Run supporting social ads geofenced to 500m around the billboard',
  ],
  weather: {
    condition: 'Clear skies · 14°C',
    visibility: 'High visibility · +4 score boost',
    visibilityScore: 'Clear',
    summary: 'Great conditions for premium static and digital creative',
  },
  traffic: {
    status: 'Evening build-up · +12% dwell time',
  },
  events: [
    {
      name: 'Fashion Forward Live Pop-up',
      date: 'Thursday · 19:00',
      venue: 'Oxford Circus Piazza',
    },
    {
      name: 'Corporate Innovation Summit',
      date: 'Friday · 09:00',
      venue: 'Regent Street Conference Centre',
    },
  ],
}
