// WorkoutCard.jsx — Single exercise card with completion toggle

export default function WorkoutCard({ exercise, index, completed, onToggle }) {
  const muscleColors = {
    'Full Body': '#38bdf8', 'Full Body Cardio': '#38bdf8',
    'Legs': '#a78bfa', 'Quads': '#a78bfa', 'Hamstrings': '#a78bfa',
    'Chest': '#fb923c', 'Upper Chest': '#fb923c',
    'Back': '#34d399', 'Mid Back': '#34d399', 'Full Posterior': '#34d399',
    'Core': '#f472b6', 'Obliques': '#f472b6', 'Core/Stability': '#f472b6',
    'Cardio': '#38bdf8', 'Full Body Cardio': '#38bdf8', 'Legs/Cardio': '#38bdf8',
    'Glutes': '#f59e0b', 'Hips/Core': '#f59e0b', 'Hips': '#f59e0b',
    'Shoulders': '#06b6d4', 'Back/Biceps': '#10b981', 'Biceps': '#10b981',
    'Triceps': '#8b5cf6', 'Spine': '#94a3b8', 'Upper Back': '#94a3b8',
    'Recovery': '#475569', 'Warm-Up': '#475569', 'Cardio': '#0ea5e9',
    'Explosive Legs': '#ef4444',
  }
  const muscleColor = muscleColors[exercise.muscle] || '#94a3b8'

  return (
    <div
      id={`exercise-card-${index}`}
      className={`exercise-card ${completed ? 'completed' : ''}`}
      onClick={onToggle}
      role="checkbox"
      aria-checked={completed}
      tabIndex={0}
      onKeyDown={e => e.key === ' ' && onToggle()}
      aria-label={`${exercise.name} - ${completed ? 'completed' : 'not completed'}`}
    >
      {/* Checkbox */}
      <div className="exercise-checkbox">
        {completed && (
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M2 6L5 9L10 3" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        )}
      </div>

      {/* Exercise Number */}
      <div style={{
        width: 32, height: 32, borderRadius: 8, flexShrink: 0,
        background: completed ? 'rgba(52,211,153,0.15)' : 'rgba(56,189,248,0.1)',
        border: `1px solid ${completed ? 'rgba(52,211,153,0.3)' : 'rgba(56,189,248,0.2)'}`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: '0.78rem', fontWeight: 800, color: completed ? '#34d399' : '#38bdf8',
        fontFamily: "'Space Grotesk', sans-serif",
      }}>
        {String(index + 1).padStart(2, '0')}
      </div>

      {/* Content */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div className="exercise-name" style={{ fontWeight: 700, fontSize: '0.95rem', marginBottom: '0.3rem' }}>
          {exercise.name}
        </div>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            <span style={{ color: 'var(--text-muted)' }}>Sets: </span>
            <strong style={{ color: 'var(--accent-cyan)' }}>{exercise.sets}</strong>
          </span>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            <span style={{ color: 'var(--text-muted)' }}>Reps: </span>
            <strong>{exercise.reps}</strong>
          </span>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            <span style={{ color: 'var(--text-muted)' }}>Rest: </span>
            <strong>{exercise.rest}</strong>
          </span>
        </div>
      </div>

      {/* Muscle Tag */}
      <div style={{
        fontSize: '0.72rem', fontWeight: 600, padding: '0.25rem 0.65rem',
        borderRadius: '999px', flexShrink: 0,
        background: `${muscleColor}18`, color: muscleColor,
        border: `1px solid ${muscleColor}30`,
      }}>
        {exercise.muscle}
      </div>

      {/* Completion indicator */}
      {completed && (
        <div style={{ fontSize: '1rem', flexShrink: 0 }}>✅</div>
      )}
    </div>
  )
}
