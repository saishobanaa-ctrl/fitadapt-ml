import { NavLink } from 'react-router-dom'

const BrainIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2a7 7 0 0 1 7 7c0 2.5-1.3 4.7-3.2 6l-.8.5V17h-6v-1.5l-.8-.5A7 7 0 0 1 12 2z"/>
    <path d="M9 17v4"/>
    <path d="M15 17v4"/>
    <path d="M9 21h6"/>
  </svg>
)

export default function Navbar() {
  return (
    <nav className="navbar" role="navigation" aria-label="Main navigation">
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1rem 1.5rem' }}>
        {/* Logo */}
        <NavLink to="/" style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', textDecoration: 'none' }}>
          <div style={{
            width: 36, height: 36, borderRadius: 10,
            background: 'linear-gradient(135deg, #0ea5e9, #8b5cf6)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 0 15px rgba(14,165,233,0.4)',
          }}>
            <span style={{ color: 'white', fontSize: '1.1rem' }}>⚡</span>
          </div>
          <span style={{
            fontFamily: "'Space Grotesk', sans-serif",
            fontWeight: 700, fontSize: '1.15rem',
            background: 'linear-gradient(135deg, #38bdf8, #a78bfa)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          }}>
            FitAdapt ML
          </span>
        </NavLink>

        {/* Links */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <NavLink to="/" end className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            Home
          </NavLink>
          <NavLink to="/predict" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            Health Predictor
          </NavLink>
          <NavLink to="/workout" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            My Workout
          </NavLink>
        </div>

        {/* CTA */}
        <NavLink to="/predict" style={{ textDecoration: 'none' }}>
          <button className="btn-primary" id="nav-get-started-btn" style={{ padding: '0.6rem 1.25rem', fontSize: '0.85rem' }}>
            <span>Get Started</span>
          </button>
        </NavLink>
      </div>
    </nav>
  )
}
