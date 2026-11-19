// ProgressBar.jsx — Animated workout completion progress bar

export default function ProgressBar({ completed, total }) {
  const pct = total > 0 ? Math.round((completed / total) * 100) : 0

  const getEmoji = () => {
    if (pct === 0)   return '🎯'
    if (pct < 33)    return '🔥'
    if (pct < 66)    return '💪'
    if (pct < 100)   return '⚡'
    return '🏆'
  }

  const getMessage = () => {
    if (pct === 0)   return 'Start your workout!'
    if (pct < 33)    return 'Great start! Keep going!'
    if (pct < 66)    return 'Halfway there — stay strong!'
    if (pct < 100)   return 'Almost done — push through!'
    return 'WORKOUT COMPLETE! Outstanding!'
  }

  return (
    <div
      id="workout-progress-bar"
      style={{
        padding: '1.5rem',
        background: pct === 100
          ? 'linear-gradient(135deg, rgba(52,211,153,0.15), rgba(56,189,248,0.15))'
          : 'rgba(0,0,0,0.3)',
        border: `1px solid ${pct === 100 ? 'rgba(52,211,153,0.4)' : 'rgba(255,255,255,0.08)'}`,
        borderRadius: 16,
        transition: 'all 0.4s ease',
      }}
    >
      {/* Top Row */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '1.25rem' }}>{getEmoji()}</span>
          <span style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-primary)' }}>
            {getMessage()}
          </span>
        </div>
        <div style={{ textAlign: 'right' }}>
          <span style={{
            fontFamily: "'Space Grotesk', sans-serif",
            fontWeight: 800, fontSize: '1.3rem',
            color: pct === 100 ? '#34d399' : 'var(--accent-cyan)',
          }}>
            {pct}%
          </span>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginLeft: '0.4rem' }}>
            {completed}/{total} exercises
          </span>
        </div>
      </div>

      {/* Track */}
      <div className="progress-track">
        <div
          className="progress-fill"
          id="progress-fill-bar"
          style={{ width: `${pct}%` }}
          role="progressbar"
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>

      {/* Milestone markers */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.4rem' }}>
        {[0, 25, 50, 75, 100].map(m => (
          <span key={m} style={{
            fontSize: '0.68rem', color: pct >= m ? 'var(--accent-cyan)' : 'var(--text-muted)',
            fontWeight: pct >= m ? 700 : 400, transition: 'color 0.3s ease',
          }}>
            {m}%
          </span>
        ))}
      </div>
    </div>
  )
}
