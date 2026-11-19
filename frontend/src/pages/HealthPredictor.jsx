import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

// Values MUST match backend schema exactly (case-sensitive)
const GOALS = [
  { value: 'Weight Loss',  label: '🔥 Weight Loss' },
  { value: 'Muscle Gain',  label: '💪 Muscle Gain' },
  { value: 'Endurance',    label: '🏃 Endurance' },
  { value: 'Flexibility',  label: '🧘 Flexibility' },
]

const EXPERIENCE = [
  { value: 'Beginner',     label: '🌱 Beginner' },
  { value: 'Intermediate', label: '⚙️ Intermediate' },
  { value: 'Advanced',     label: '🏆 Advanced' },
]

const EQUIPMENT = [
  { value: 'None',     label: '🏠 No Equipment' },
  { value: 'Minimal',  label: '🪢 Minimal Equipment' },
  { value: 'Full Gym', label: '🏋️ Full Gym' },
]

// Keys MUST match backend PcodSymptoms schema exactly
const PCOD_INDICATORS = [
  { key: 'cycle_irregularity', label: 'Irregular Menstrual Cycles', desc: 'Cycles shorter than 21 days or longer than 35 days' },
  { key: 'stubborn_weight',    label: 'Stubborn Weight Retention',  desc: 'Difficulty losing weight despite consistent effort' },
  { key: 'hirsutism',         label: 'Excess Facial/Body Hair',    desc: 'Unusual hair growth on face, chest, or back' },
  { key: 'acne',              label: 'Persistent Hormonal Acne',   desc: 'Acne concentrated on jaw, chin, or back' },
  { key: 'acanthosis',        label: 'Skin Darkening (Acanthosis Nigricans)', desc: 'Dark patches at neck, underarms, or groin' },
]

function Toggle({ value, onChange, id }) {
  return (
    <div
      id={id}
      className={`toggle-track ${value ? 'active' : ''}`}
      role="checkbox"
      aria-checked={value}
      tabIndex={0}
      onClick={() => onChange(!value)}
      onKeyDown={e => e.key === ' ' && onChange(!value)}
      style={{ cursor: 'pointer' }}
    >
      <div className="toggle-thumb" />
    </div>
  )
}

function FormField({ label, children, hint }) {
  return (
    <div className="form-group">
      <label className="form-label">{label}</label>
      {children}
      {hint && <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{hint}</span>}
    </div>
  )
}

export default function HealthPredictor() {
  const navigate = useNavigate()
  const riskRef = useRef(null)

  const [form, setForm] = useState({
    age: '', gender: '', weight: '', height: '',
    goal: '', experience_level: '', equipment: '',
    training_days: '', session_duration: '',
  })

  const [pcod, setPcod] = useState({
    cycle_irregularity: false, stubborn_weight: false,
    hirsutism: false, acne: false,
    acanthosis: false,
  })

  const [loading, setLoading]     = useState(false)
  const [error, setError]         = useState(null)
  const [result, setResult]       = useState(null)

  const isFemale = form.gender === 'Female'

  const handleChange = (field, value) => {
    setForm(prev => ({ ...prev, [field]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // Map form fields → backend schema field names exactly
      const payload = {
        age:                    parseInt(form.age),
        gender:                 form.gender,          // 'Male' | 'Female' | 'Other'
        weight_kg:              parseFloat(form.weight),
        height_cm:              parseFloat(form.height),
        fitness_goal:           form.goal,            // 'Weight Loss' | 'Muscle Gain' etc.
        experience_level:       form.experience_level, // 'Beginner' | 'Intermediate' | 'Advanced'
        equipment:              form.equipment,        // 'None' | 'Minimal' | 'Full Gym'
        training_days_per_week: parseInt(form.training_days),
        session_duration_min:   parseInt(form.session_duration),
        pcod_symptoms:          isFemale ? pcod : null,
      }

      const res = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(JSON.stringify(err.detail) || 'Prediction failed')
      }

      const data = await res.json()
      setResult(data)

      // Persist workout data to sessionStorage for MyWorkout page
      sessionStorage.setItem('fitadapt_plan', JSON.stringify({
        name: data.plan_name,
        quality_score: data.quality_score,
        exercises: data.workout_plan,
        cluster_id: data.cluster_id,
        // Template metadata for workout page display
        goal: data.fitness_goal,
        experience_level: data.experience_level,
        equipment: data.equipment,
        volume_score: data.volume_score   !== undefined ? data.volume_score / 10   : null,
        intensity_score: data.intensity_score !== undefined ? data.intensity_score / 10 : null,
      }))
      sessionStorage.setItem('fitadapt_cluster', data.cluster_id)

      // Scroll to results
      setTimeout(() => {
        riskRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 100)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const selectStyle = (field) => ({
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
    gap: '0.6rem',
  })

  const OptionBtn = ({ value, label, field, current }) => (
    <button
      type="button"
      id={`${field}-${value}-btn`}
      onClick={() => handleChange(field, value)}
      style={{
        padding: '0.75rem 1rem',
        borderRadius: 10,
        border: `1px solid ${current === value ? 'var(--accent-cyan)' : 'rgba(99,179,237,0.15)'}`,
        background: current === value ? 'rgba(56,189,248,0.12)' : 'rgba(17,24,39,0.6)',
        color: current === value ? 'var(--accent-cyan)' : 'var(--text-secondary)',
        fontWeight: current === value ? 700 : 400,
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        fontSize: '0.9rem',
        textAlign: 'center',
      }}
    >
      {label}
    </button>
  )

  return (
    <div style={{ minHeight: '100vh', padding: '3rem 1.5rem 5rem' }}>
      <div className="container" style={{ maxWidth: 760 }}>
        {/* Page Header */}
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <span className="badge badge-blue" style={{ marginBottom: '1rem', display: 'inline-block' }}>
            🤖 ML-Powered Analysis
          </span>
          <h1 className="heading-hero" style={{ fontSize: 'clamp(2rem, 4vw, 2.8rem)', marginBottom: '0.75rem' }}>
            Health Risk &{' '}
            <span className="text-gradient">Workout Predictor</span>
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1rem', maxWidth: 500, margin: '0 auto' }}>
            Fill in your biometrics to run the K-Means + Random Forest pipeline and receive your personalized risk report.
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} id="health-predictor-form" aria-label="Health predictor form">
          <div className="glass-card" style={{ padding: '2rem', display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>

            {/* ── Section: Core Biometrics ── */}
            <div>
              <div className="section-divider">
                <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.1em', whiteSpace: 'nowrap' }}>
                  Core Biometrics
                </span>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.25rem' }}>
                <FormField label="Age (years)">
                  <input id="input-age" type="number" className="form-input" placeholder="e.g. 24"
                    min={10} max={100} value={form.age} required
                    onChange={e => handleChange('age', e.target.value)} />
                </FormField>

                <FormField label="Weight (kg)">
                  <input id="input-weight" type="number" className="form-input" placeholder="e.g. 68"
                    min={20} max={300} step={0.1} value={form.weight} required
                    onChange={e => handleChange('weight', e.target.value)} />
                </FormField>

                <FormField label="Height (cm)">
                  <input id="input-height" type="number" className="form-input" placeholder="e.g. 170"
                    min={100} max={250} value={form.height} required
                    onChange={e => handleChange('height', e.target.value)} />
                </FormField>
              </div>
            </div>

            {/* ── Gender ── */}
            <FormField label="Gender">
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.6rem' }}>
                {[{ value: 'Male', label: '♂ Male' }, { value: 'Female', label: '♀ Female' }, { value: 'Other', label: '⚧ Other' }].map(g => (
                  <OptionBtn key={g.value} value={g.value} label={g.label} field="gender" current={form.gender} />
                ))}
              </div>
            </FormField>

            {/* ── Fitness Goal ── */}
            <FormField label="Fitness Goal">
              <div style={selectStyle('goal')}>
                {GOALS.map(g => (
                  <OptionBtn key={g.value} value={g.value} label={g.label} field="goal" current={form.goal} />
                ))}
              </div>
            </FormField>

            {/* ── Experience & Equipment ── */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem' }}>
              <FormField label="Experience Level">
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {EXPERIENCE.map(e => (
                    <OptionBtn key={e.value} value={e.value} label={e.label} field="experience_level" current={form.experience_level} />
                  ))}
                </div>
              </FormField>

              <FormField label="Equipment Available">
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {EQUIPMENT.map(e => (
                    <OptionBtn key={e.value} value={e.value} label={e.label} field="equipment" current={form.equipment} />
                  ))}
                </div>
              </FormField>
            </div>

            {/* ── Training Schedule ── */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.25rem' }}>
              <FormField label="Training Days / Week" hint="0 = sedentary, 7 = daily">
                <input id="input-training-days" type="number" className="form-input"
                  placeholder="e.g. 4" min={0} max={7} value={form.training_days} required
                  onChange={e => handleChange('training_days', e.target.value)} />
              </FormField>

              <FormField label="Session Duration (min)" hint="Per workout session">
                <input id="input-session-duration" type="number" className="form-input"
                  placeholder="e.g. 45" min={10} max={180} value={form.session_duration} required
                  onChange={e => handleChange('session_duration', e.target.value)} />
              </FormField>
            </div>

            {/* ── PCOD/PCOS Section (Female only) ── */}
            {isFemale && (
              <div style={{ animation: 'fade-in 0.4s ease' }}>
                <div className="section-divider">
                  <span style={{ fontSize: '0.8rem', fontWeight: 700, color: '#f472b6', textTransform: 'uppercase', letterSpacing: '0.1em', whiteSpace: 'nowrap' }}>
                    💜 PCOD / PCOS Screening
                  </span>
                </div>

                <div style={{
                  background: 'rgba(244,114,182,0.05)', border: '1px solid rgba(244,114,182,0.2)',
                  borderRadius: 14, padding: '1.25rem', marginBottom: '1rem',
                }}>
                  <p style={{ color: '#f9a8d4', fontSize: '0.85rem', lineHeight: 1.6 }}>
                    <strong>Women's Health Module:</strong> Toggle any indicators that apply to you.
                    This optional screening helps our engine compute your endocrine risk score for
                    PCOD/PCOS predisposition — a preventative awareness tool, not a diagnosis.
                  </p>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {PCOD_INDICATORS.map((ind) => (
                    <div
                      key={ind.key}
                      id={`pcod-${ind.key}`}
                      style={{
                        display: 'flex', alignItems: 'center', gap: '1rem',
                        padding: '0.9rem 1rem', borderRadius: 12,
                        background: pcod[ind.key] ? 'rgba(244,114,182,0.08)' : 'rgba(0,0,0,0.2)',
                        border: `1px solid ${pcod[ind.key] ? 'rgba(244,114,182,0.3)' : 'rgba(255,255,255,0.06)'}`,
                        transition: 'all 0.2s ease', cursor: 'pointer',
                      }}
                      onClick={() => setPcod(prev => ({ ...prev, [ind.key]: !prev[ind.key] }))}
                    >
                      <Toggle
                        id={`toggle-${ind.key}`}
                        value={pcod[ind.key]}
                        onChange={(v) => setPcod(prev => ({ ...prev, [ind.key]: v }))}
                      />
                      <div>
                        <div style={{ fontWeight: 600, fontSize: '0.9rem', color: pcod[ind.key] ? '#f472b6' : 'var(--text-primary)' }}>
                          {ind.label}
                        </div>
                        <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                          {ind.desc}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Error */}
            {error && (
              <div style={{
                padding: '1rem', borderRadius: 10, background: 'rgba(239,68,68,0.1)',
                border: '1px solid rgba(239,68,68,0.3)', color: '#f87171', fontSize: '0.9rem',
              }}>
                ⚠️ {error}
                <br />
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.3rem', display: 'block' }}>
                  Make sure the backend server is running: <code style={{ color: 'var(--accent-cyan)' }}>uvicorn main:app --reload</code>
                </span>
              </div>
            )}

            {/* Submit */}
            <button
              id="submit-predict-btn"
              type="submit"
              className="btn-primary"
              disabled={loading}
              style={{ width: '100%', padding: '1.1rem', fontSize: '1rem', opacity: loading ? 0.7 : 1 }}
            >
              {loading ? (
                <span style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', justifyContent: 'center' }}>
                  <div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }} />
                  <span>Running ML Pipeline...</span>
                </span>
              ) : (
                <span>🚀 Run Health Analysis & Get My Workout</span>
              )}
            </button>
          </div>
        </form>

        {/* ── Results ── */}
        {result && (
          <div ref={riskRef} style={{ marginTop: '2.5rem' }}>
            {/* ML Summary Card */}
            <div className="glass-card" style={{ padding: '1.5rem', marginBottom: '1.5rem', borderColor: 'rgba(0,212,255,0.3)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
                <span style={{ fontSize: '1.5rem' }}>🤖</span>
                <h2 style={{ margin: 0, fontSize: '1.3rem', color: 'var(--accent-cyan)' }}>ML Analysis Complete</h2>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem' }}>
                <div style={{ textAlign: 'center', padding: '0.75rem', background: 'rgba(0,212,255,0.08)', borderRadius: 10 }}>
                  <div style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>#{result.cluster_id}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>K-Means Cluster</div>
                </div>
                <div style={{ textAlign: 'center', padding: '0.75rem', background: 'rgba(124,58,237,0.08)', borderRadius: 10 }}>
                  <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#a78bfa' }}>{result.quality_score}/100</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Plan Quality Score</div>
                </div>
                <div style={{ textAlign: 'center', padding: '0.75rem', background: 'rgba(16,185,129,0.08)', borderRadius: 10 }}>
                  <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#34d399' }}>{result.bmi}</div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>BMI — {result.bmi_category}</div>
                </div>
              </div>
              <div style={{ marginTop: '0.75rem', padding: '0.6rem 1rem', background: 'rgba(0,0,0,0.3)', borderRadius: 8, fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                📋 Plan: <strong style={{ color: 'var(--text-primary)' }}>{result.plan_name}</strong>
              </div>
            </div>

            {/* Risk Flags */}
            {result.risk_flags?.length > 0 && (
              <div className="glass-card" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
                <h3 style={{ marginTop: 0, color: '#fbbf24' }}>⚠️ Preventative Health Risk Analysis</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                  {result.risk_flags.map((flag, i) => (
                    <div key={i} style={{
                      padding: '1rem', borderRadius: 10,
                      borderLeft: `4px solid ${flag.severity === 'high' ? '#ef4444' : flag.severity === 'medium' ? '#f59e0b' : '#eab308'}`,
                      background: flag.severity === 'high' ? 'rgba(239,68,68,0.08)' : flag.severity === 'medium' ? 'rgba(245,158,11,0.08)' : 'rgba(234,179,8,0.08)',
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.3rem' }}>
                        <strong style={{ color: 'var(--text-primary)' }}>{flag.title}</strong>
                        <span style={{
                          fontSize: '0.72rem', fontWeight: 700, padding: '2px 8px', borderRadius: 20,
                          background: flag.severity === 'high' ? 'rgba(239,68,68,0.2)' : flag.severity === 'medium' ? 'rgba(245,158,11,0.2)' : 'rgba(234,179,8,0.2)',
                          color: flag.severity === 'high' ? '#f87171' : flag.severity === 'medium' ? '#fbbf24' : '#fde047',
                          textTransform: 'uppercase',
                        }}>{flag.severity}</span>
                      </div>
                      <p style={{ margin: 0, fontSize: '0.85rem', color: 'var(--text-secondary)' }}>{flag.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* PCOD Section */}
            {result.pcod_risk_score !== null && result.pcod_risk_score !== undefined && (
              <div className="glass-card" style={{ padding: '1.5rem', marginBottom: '1.5rem', borderColor: 'rgba(244,114,182,0.3)' }}>
                <h3 style={{ marginTop: 0, color: '#f472b6' }}>🔬 PCOD/PCOS Endocrine Risk Assessment</h3>
                <div style={{ marginBottom: '0.75rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
                    <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Risk Score</span>
                    <span style={{ fontWeight: 700, color: '#f472b6' }}>{result.pcod_risk_score}/100 — {result.pcod_risk_level}</span>
                  </div>
                  <div style={{ height: 8, background: 'rgba(255,255,255,0.1)', borderRadius: 4, overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: `${result.pcod_risk_score}%`, background: 'linear-gradient(90deg,#f472b6,#ec4899)', borderRadius: 4, transition: 'width 1s ease' }} />
                  </div>
                </div>
                <p style={{ margin: 0, fontSize: '0.83rem', color: '#f9a8d4' }}>
                  This is a preventative awareness score — not a clinical diagnosis. Please consult a gynaecologist or endocrinologist for professional evaluation.
                </p>
              </div>
            )}

            {/* Recommendations */}
            {result.recommendations?.length > 0 && (
              <div className="glass-card" style={{ padding: '1.5rem', marginBottom: '1.5rem' }}>
                <h3 style={{ marginTop: 0, color: '#34d399' }}>✅ Recommendations</h3>
                <ul style={{ margin: 0, paddingLeft: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  {result.recommendations.map((r, i) => (
                    <li key={i} style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.5 }}>{r}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Motivational CTA */}
            <div style={{
              padding: '2rem', borderRadius: 16, textAlign: 'center',
              background: 'linear-gradient(135deg, rgba(0,212,255,0.12), rgba(124,58,237,0.12))',
              border: '1px solid rgba(0,212,255,0.3)',
            }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>🏃</div>
              <h2 style={{ margin: '0 0 0.5rem', color: 'var(--text-primary)' }}>Start Doing Your Exercises Now!</h2>
              <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
                Your personalized workout plan is ready based on your ML Cluster #{result.cluster_id} profile.
              </p>
              <button
                id="go-to-workout-btn"
                className="btn-primary"
                onClick={() => navigate('/workout')}
                style={{ fontSize: '1rem', padding: '1rem 2.5rem' }}
              >
                <span>💪 View My Personalized Workout →</span>
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
