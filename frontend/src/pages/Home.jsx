import { useNavigate } from 'react-router-dom'

const features = [
  {
    icon: '🧬',
    title: 'K-Means User Clustering',
    desc: 'Unsupervised ML groups you into one of 5 behavioral and physiological archetypes using your biometrics and lifestyle data — evaluated with Silhouette Score.',
    colorClass: 'feature-card-cyan',
    iconBg: 'linear-gradient(135deg, rgba(56,189,248,0.2), rgba(56,189,248,0.05))',
    iconColor: '#38bdf8',
    tag: 'Unsupervised Learning',
  },
  {
    icon: '🤖',
    title: 'Random Forest Plan Scoring',
    desc: 'A supervised regression model predicts the Plan Quality Score (0–100) for every workout template against your profile — optimized via RMSE & R² metrics.',
    colorClass: 'feature-card-violet',
    iconBg: 'linear-gradient(135deg, rgba(167,139,250,0.2), rgba(167,139,250,0.05))',
    iconColor: '#a78bfa',
    tag: 'Supervised Learning',
  },
  {
    icon: '🩺',
    title: 'Preventative Health Engine',
    desc: 'Clinical heuristics stratify your risk for Type-2 Diabetes, joint stress, and PCOD/PCOS — delivering targeted preventative awareness before symptoms emerge.',
    colorClass: 'feature-card-green',
    iconBg: 'linear-gradient(135deg, rgba(52,211,153,0.2), rgba(52,211,153,0.05))',
    iconColor: '#34d399',
    tag: 'Health AI',
  },
]

const stats = [
  { value: '5', label: 'User Archetypes', icon: '👥' },
  { value: '13', label: 'Workout Templates', icon: '📋' },
  { value: '3', label: 'Risk Modules', icon: '🛡️' },
  { value: '6', label: 'PCOD Indicators', icon: '💜' },
]

export default function Home() {
  const navigate = useNavigate()

  return (
    <div style={{ minHeight: '100vh' }}>
      {/* ─── HERO SECTION ─── */}
      <section
        style={{ padding: '7rem 1.5rem 5rem', textAlign: 'center' }}
        aria-labelledby="hero-heading"
      >
        <div className="container">
          {/* Badge */}
          <div className="animate-fade-in" style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'center' }}>
            <span className="badge badge-blue" style={{ fontSize: '0.8rem', padding: '0.4rem 1rem' }}>
              🎓 &nbsp; ML Curriculum Project — 3rd Year
            </span>
          </div>

          {/* Headline */}
          <h1
            id="hero-heading"
            className="heading-hero animate-fade-in-delay-1"
            style={{ fontSize: 'clamp(2.5rem, 6vw, 4.5rem)', marginBottom: '1.5rem' }}
          >
            <span className="text-gradient">AI-Powered</span>
            <br />
            <span style={{ color: 'var(--text-primary)' }}>Fitness Intelligence</span>
          </h1>

          {/* Subtitle */}
          <p
            className="animate-fade-in-delay-2"
            style={{
              fontSize: '1.15rem', color: 'var(--text-secondary)',
              maxWidth: 620, margin: '0 auto 2.5rem',
              lineHeight: 1.8,
            }}
          >
            FitAdapt ML clusters your profile with K-Means, scores workout plans via Random Forest,
            and delivers a preventative health risk report — all powered by a production-grade
            FastAPI + scikit-learn pipeline.
          </p>

          {/* CTA Buttons */}
          <div className="animate-fade-in-delay-3" style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <button
              id="hero-start-btn"
              className="btn-primary"
              onClick={() => navigate('/predict')}
              style={{ fontSize: '1rem', padding: '1rem 2.5rem' }}
            >
              <span>⚡ Start Health Analysis</span>
            </button>
            <button
              id="hero-workout-btn"
              className="btn-secondary"
              onClick={() => navigate('/workout')}
            >
              View My Workout
            </button>
          </div>

          {/* Stats Row */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
              gap: '1rem',
              maxWidth: 700,
              margin: '4rem auto 0',
            }}
          >
            {stats.map((s, i) => (
              <div
                key={s.label}
                className="stat-box animate-fade-in"
                style={{ animationDelay: `${0.4 + i * 0.1}s` }}
              >
                <div style={{ fontSize: '1.5rem', marginBottom: '0.4rem' }}>{s.icon}</div>
                <div style={{ fontSize: '1.8rem', fontWeight: 800, fontFamily: "'Space Grotesk', sans-serif", color: 'var(--accent-cyan)' }}>
                  {s.value}
                </div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  {s.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── FEATURES SECTION ─── */}
      <section style={{ padding: '3rem 1.5rem 5rem' }} aria-labelledby="features-heading">
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <h2
              id="features-heading"
              style={{ fontSize: '2rem', fontWeight: 800, fontFamily: "'Space Grotesk', sans-serif", marginBottom: '0.75rem' }}
            >
              The ML Pipeline
            </h2>
            <p style={{ color: 'var(--text-secondary)', maxWidth: 500, margin: '0 auto' }}>
              Three intelligent modules working in concert to deliver personalized, medically-aware fitness guidance.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
            {features.map((f, i) => (
              <article
                key={f.title}
                className={`feature-card ${f.colorClass}`}
                style={{ animationDelay: `${i * 0.1}s` }}
              >
                {/* Tag */}
                <div style={{ marginBottom: '1rem' }}>
                  <span style={{
                    fontSize: '0.7rem', fontWeight: 700, letterSpacing: '0.08em',
                    textTransform: 'uppercase', color: f.iconColor,
                    background: `${f.iconBg}`, padding: '0.25rem 0.75rem',
                    borderRadius: '999px', border: `1px solid ${f.iconColor}30`,
                  }}>
                    {f.tag}
                  </span>
                </div>

                {/* Icon */}
                <div
                  className="feature-icon"
                  style={{ background: f.iconBg, border: `1px solid ${f.iconColor}25` }}
                >
                  {f.icon}
                </div>

                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.75rem' }}>
                  {f.title}
                </h3>
                <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.7 }}>
                  {f.desc}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* ─── HOW IT WORKS ─── */}
      <section style={{ padding: '0 1.5rem 6rem' }} aria-labelledby="how-heading">
        <div className="container">
          <div className="glass-card" style={{ padding: '3rem' }}>
            <h2
              id="how-heading"
              style={{ fontSize: '1.75rem', fontWeight: 800, fontFamily: "'Space Grotesk', sans-serif", textAlign: 'center', marginBottom: '2.5rem' }}
            >
              How It Works
            </h2>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem', textAlign: 'center' }}>
              {[
                { step: '01', label: 'Input Biometrics', desc: 'Enter age, weight, height, goal, experience & equipment', icon: '📝' },
                { step: '02', label: 'Cluster Assignment', desc: 'K-Means assigns your user archetype cluster (k=5)', icon: '🔵' },
                { step: '03', label: 'Plan Scoring', desc: 'Random Forest scores all 13 templates → picks best', icon: '📊' },
                { step: '04', label: 'Risk Analysis', desc: 'Health engine stratifies diabetes, joint & PCOD risk', icon: '🛡️' },
                { step: '05', label: 'Your Plan', desc: 'Receive personalized workout + risk-aware health advice', icon: '✅' },
              ].map((item, i) => (
                <div key={item.step} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem' }}>
                  <div style={{
                    width: 56, height: 56, borderRadius: '50%',
                    background: 'linear-gradient(135deg, rgba(56,189,248,0.15), rgba(167,139,250,0.15))',
                    border: '1px solid rgba(56,189,248,0.2)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '1.5rem',
                  }}>
                    {item.icon}
                  </div>
                  <div style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--accent-cyan)', letterSpacing: '0.1em' }}>
                    STEP {item.step}
                  </div>
                  <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>{item.label}</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.82rem', lineHeight: 1.6 }}>{item.desc}</div>
                </div>
              ))}
            </div>

            <div style={{ textAlign: 'center', marginTop: '2.5rem' }}>
              <button
                id="how-cta-btn"
                className="btn-primary"
                onClick={() => navigate('/predict')}
                style={{ fontSize: '1rem', padding: '1rem 2.5rem' }}
              >
                <span>🚀 Launch Health Predictor</span>
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
