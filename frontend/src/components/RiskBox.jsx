// RiskBox.jsx — Preventative Health Risk Report Component

const riskColors = {
  'Low':       { bg: 'rgba(52,211,153,0.08)', border: 'rgba(52,211,153,0.3)', text: '#34d399', badgeClass: 'badge-low' },
  'Moderate':  { bg: 'rgba(251,146,60,0.08)', border: 'rgba(251,146,60,0.3)',  text: '#fb923c', badgeClass: 'badge-moderate' },
  'High':      { bg: 'rgba(248,113,113,0.08)', border: 'rgba(248,113,113,0.3)', text: '#f87171', badgeClass: 'badge-high' },
  'Very High': { bg: 'rgba(239,68,68,0.12)', border: 'rgba(239,68,68,0.4)',  text: '#ef4444', badgeClass: 'badge-very-high' },
}

function RiskBadge({ level }) {
  const c = riskColors[level] || riskColors['Low']
  return <span className={`badge ${c.badgeClass}`}>● {level} Risk</span>
}

function RiskModule({ title, icon, risk, children }) {
  const c = riskColors[risk?.risk_level] || riskColors['Low']
  return (
    <div className="risk-module" style={{ borderColor: c.border, background: c.bg }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ fontSize: '1.2rem' }}>{icon}</span>
          <span style={{ fontWeight: 700, fontSize: '0.95rem' }}>{title}</span>
        </div>
        {risk && <RiskBadge level={risk.risk_level} />}
      </div>
      {children}
    </div>
  )
}

export default function RiskBox({ riskReport, clusterId, planName, qualityScore }) {
  if (!riskReport) return null

  const { bmi_info, metabolic, joint, pcod, overall_risk, motivational_message } = riskReport
  const overallColor = riskColors[overall_risk] || riskColors['Low']

  return (
    <div className="risk-box" id="risk-report-section" aria-label="Health Risk Report">
      {/* ── Header ── */}
      <div style={{
        background: 'linear-gradient(135deg, #1a1040 0%, #0d1a30 100%)',
        border: '1px solid rgba(167,139,250,0.2)',
        borderRadius: 20, padding: '1.75rem', marginBottom: '1.25rem',
      }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '1.4rem' }}>🛡️</span>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 800, fontFamily: "'Space Grotesk', sans-serif" }}>
                Health Risk Analysis
              </h2>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
              Preventative health stratification based on your biometrics
            </p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.3rem', textTransform: 'uppercase', letterSpacing: '0.08em' }}>Overall Risk</div>
            <span className={`badge ${overallColor.badgeClass}`} style={{ fontSize: '0.85rem' }}>
              {overall_risk}
            </span>
          </div>
        </div>

        {/* BMI Strip */}
        <div style={{
          marginTop: '1.25rem', padding: '0.85rem 1.25rem',
          background: 'rgba(0,0,0,0.3)', borderRadius: 12,
          display: 'flex', alignItems: 'center', gap: '1.5rem', flexWrap: 'wrap',
        }}>
          <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.07em' }}>BMI</div>
            <div style={{ fontSize: '1.6rem', fontWeight: 800, fontFamily: "'Space Grotesk', sans-serif", color: 'var(--accent-cyan)' }}>
              {bmi_info.bmi}
            </div>
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.2rem' }}>Classification</div>
            <div style={{ fontWeight: 700, color: 'var(--text-primary)' }}>{bmi_info.category}</div>
          </div>
          {clusterId !== undefined && (
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Cluster</div>
              <div style={{ fontWeight: 800, fontSize: '1.3rem', color: 'var(--accent-violet)' }}>#{clusterId}</div>
            </div>
          )}
        </div>
      </div>

      {/* ── Risk Modules ── */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1.25rem' }}>

        {/* Metabolic Risk */}
        <RiskModule title="Type-2 Diabetes / Insulin Resistance" icon="🩸" risk={metabolic}>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.87rem', marginBottom: '0.75rem', lineHeight: 1.6 }}>
            {metabolic.message}
          </p>
          {metabolic.factors.length > 0 && (
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
              {metabolic.factors.map((f, i) => (
                <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem', fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                  <span style={{ color: '#fb923c', flexShrink: 0 }}>⚠</span> {f}
                </li>
              ))}
            </ul>
          )}
        </RiskModule>

        {/* Joint Stress Risk */}
        <RiskModule title="Joint Strain / Osteoarthritis Predisposition" icon="🦴" risk={joint}>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.87rem', marginBottom: '0.75rem', lineHeight: 1.6 }}>
            {joint.message}
          </p>
          {joint.factors.length > 0 && (
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
              {joint.factors.map((f, i) => (
                <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '0.5rem', fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                  <span style={{ color: '#f87171', flexShrink: 0 }}>⚠</span> {f}
                </li>
              ))}
            </ul>
          )}
        </RiskModule>

        {/* PCOD/PCOS (female only) */}
        {pcod && (
          <RiskModule title="PCOD / PCOS Endocrine Screening" icon="💜" risk={pcod}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                Indicators triggered:
              </span>
              <span style={{
                fontWeight: 800, fontSize: '1.1rem', color: '#f472b6',
                fontFamily: "'Space Grotesk', sans-serif",
              }}>
                {pcod.score} / {pcod.max_score}
              </span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.87rem', marginBottom: '0.75rem', lineHeight: 1.6 }}>
              {pcod.message}
            </p>
            {pcod.positive_indicators.length > 0 && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginBottom: '0.75rem' }}>
                {pcod.positive_indicators.map((ind, i) => (
                  <span key={i} style={{
                    fontSize: '0.75rem', background: 'rgba(244,114,182,0.12)',
                    color: '#f472b6', border: '1px solid rgba(244,114,182,0.25)',
                    padding: '0.2rem 0.6rem', borderRadius: '6px', fontWeight: 600,
                  }}>
                    {ind}
                  </span>
                ))}
              </div>
            )}
            <div style={{
              padding: '0.85rem', borderRadius: 10,
              background: 'rgba(244,114,182,0.08)', border: '1px solid rgba(244,114,182,0.2)',
              fontSize: '0.83rem', color: '#f9a8d4', lineHeight: 1.6,
            }}>
              <strong>Recommendation:</strong> {pcod.recommendation}
            </div>
          </RiskModule>
        )}
      </div>

      {/* ── Motivational Banner ── */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(14,165,233,0.15), rgba(139,92,246,0.15))',
        border: '1px solid rgba(99,179,237,0.25)',
        borderRadius: 16, padding: '1.5rem',
        textAlign: 'center',
      }}>
        <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>💪</div>
        <p style={{
          fontWeight: 700, fontSize: '1rem',
          fontFamily: "'Space Grotesk', sans-serif",
          color: 'var(--text-primary)', marginBottom: '0.5rem', lineHeight: 1.5,
        }}>
          {motivational_message}
        </p>
        {planName && (
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
            Your recommended plan: <strong style={{ color: 'var(--accent-cyan)' }}>{planName}</strong>
            {qualityScore !== undefined && (
              <span style={{ color: 'var(--accent-green)', marginLeft: '0.5rem' }}>
                (Quality Score: {qualityScore.toFixed(1)}/100)
              </span>
            )}
          </p>
        )}
      </div>
    </div>
  )
}
