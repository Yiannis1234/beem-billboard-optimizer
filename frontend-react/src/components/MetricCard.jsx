import PropTypes from 'prop-types'

const accentStyles = {
  blue: 'from-blue-500/10 to-blue-500/5 border-blue-100 text-blue-700',
  green: 'from-emerald-500/10 to-emerald-500/5 border-emerald-100 text-emerald-700',
  purple: 'from-violet-500/10 to-violet-500/5 border-violet-100 text-violet-700',
  orange: 'from-orange-500/10 to-orange-500/5 border-orange-100 text-orange-700',
}

const MetricCard = ({ label, value, suffix, helper, accent = 'blue' }) => {
  const accentClass = accentStyles[accent] ?? accentStyles.blue

  return (
    <div className={`flex h-full flex-col justify-between rounded-xl border bg-gradient-to-br ${accentClass} p-4 shadow-sm sm:rounded-2xl sm:p-5`}>
      <span className="text-xs font-semibold uppercase tracking-wide text-slate-500 sm:text-sm">{label}</span>
      <div className="mt-2 flex items-end gap-2">
        <span className="text-2xl font-black text-slate-900 sm:text-3xl md:text-4xl">{value}</span>
        {suffix ? <span className="pb-0.5 text-xs font-semibold text-slate-500 sm:pb-1 sm:text-sm">{suffix}</span> : null}
      </div>
      {helper ? <p className="mt-2 text-xs text-slate-600 sm:mt-3 sm:text-sm">{helper}</p> : null}
    </div>
  )
}

MetricCard.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  suffix: PropTypes.string,
  helper: PropTypes.string,
  accent: PropTypes.oneOf(['blue', 'green', 'purple', 'orange']),
}

export default MetricCard
