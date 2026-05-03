import ForecastChart from '../components/ForecastChart'
import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'

export default function ForecastPage() {
  const { user } = useAuth()

  if (!user) {
    return (
      <div className="container mt-4 text-center py-5">
        <h4 className="text-muted">Please log in to view forecasts.</h4>
        <Link to="/login" className="btn btn-dark mt-3">Login</Link>
      </div>
    )
  }

  return (
    <div className="container mt-4">
      <div className="d-flex align-items-center gap-2 mb-4">
        <h2 className="mb-0">Sales Forecast</h2>
        <span className="badge bg-purple text-white" style={{ background: '#7F77DD' }}>
          ML powered
        </span>
      </div>
      <ForecastChart />
    </div>
  )
}