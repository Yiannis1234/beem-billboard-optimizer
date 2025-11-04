import PropTypes from 'prop-types'

const SelectField = ({
  label,
  value,
  onChange,
  options = [],
  helperText,
  placeholder = 'Select an option',
  disabled = false,
}) => {
  const hasOptions = options && options.length > 0
  const isDisabled = disabled || !hasOptions

  return (
    <label className="flex w-full flex-col gap-2 text-sm font-medium text-slate-700">
      <span>{label}</span>
      <select
        value={value ?? ''}
        onChange={(event) => onChange(event.target.value)}
        disabled={isDisabled}
        className={`w-full rounded-xl border-2 px-4 py-3 text-base font-semibold shadow-sm transition focus:outline-none focus:ring-4 ${
          isDisabled
            ? 'cursor-not-allowed border-slate-200 bg-slate-100 text-slate-400'
            : 'border-slate-200 bg-white text-slate-800 focus:border-blue-500 focus:ring-blue-100'
        }`}
      >
        <option value="" disabled>
          {hasOptions ? placeholder : 'Loading options…'}
        </option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {helperText ? <span className="text-xs font-normal text-slate-500">{helperText}</span> : null}
    </label>
  )
}

SelectField.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.string,
  onChange: PropTypes.func.isRequired,
  options: PropTypes.arrayOf(
    PropTypes.shape({
      value: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
    })
  ),
  helperText: PropTypes.string,
  placeholder: PropTypes.string,
  disabled: PropTypes.bool,
}

export default SelectField
