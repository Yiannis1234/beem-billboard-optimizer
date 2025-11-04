import PropTypes from 'prop-types'

const SectionCard = ({ title, description, children, actions }) => {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm lg:p-8">
      <div className="flex flex-col gap-3 border-b border-slate-100 pb-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900 lg:text-2xl">{title}</h2>
          {description ? <p className="mt-1 text-sm text-slate-600 lg:text-base">{description}</p> : null}
        </div>
        {actions ? <div className="flex flex-wrap items-center gap-3">{actions}</div> : null}
      </div>
      <div className="mt-6 space-y-6 lg:space-y-8">{children}</div>
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
