import PropTypes from 'prop-types'

const SectionCard = ({ title, description, children, actions }) => {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:rounded-3xl sm:p-6 lg:p-8">
      <div className="flex flex-col gap-2 border-b border-slate-100 pb-4 sm:gap-3 sm:pb-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-900 sm:text-xl lg:text-2xl">{title}</h2>
          {description ? <p className="mt-1 text-xs text-slate-600 sm:text-sm lg:text-base">{description}</p> : null}
        </div>
        {actions ? <div className="flex flex-wrap items-center gap-2 sm:gap-3">{actions}</div> : null}
      </div>
      <div className="mt-4 space-y-4 sm:mt-6 sm:space-y-6 lg:space-y-8">{children}</div>
    </section>
  )
}

SectionCard.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.string,
  children: PropTypes.node,
  actions: PropTypes.node,
}

export default SectionCard
