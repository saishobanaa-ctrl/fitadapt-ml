import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import HealthPredictor from './pages/HealthPredictor'
import MyWorkout from './pages/MyWorkout'

export default function App() {
  return (
    <>
      <div className="animated-bg" aria-hidden="true" />
      <Navbar />
      <main>
        <Routes>
          <Route path="/"         element={<Home />} />
          <Route path="/predict"  element={<HealthPredictor />} />
          <Route path="/workout"  element={<MyWorkout />} />
        </Routes>
      </main>
    </>
  )
}
