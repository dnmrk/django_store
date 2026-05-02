import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useQuery } from '@tanstack/react-query'
import { getOrders } from '../api/orders'

export default function ProfilePage() {
  const { user, logout } = useAuth()

  const { data: orders } = useQuery({
    queryKey: ['orders'],
    queryFn: getOrders,
  })

  return (
    <div className="container mt-4">
      <div className="row justify-content-center">
        <div className="col-md-6">

          <div className="card shadow-sm mb-4">
            <div className="card-body p-4">
              <h3 className="mb-4">My Profile</h3>
              <p><strong>Username:</strong> {user?.username}</p>
              <p><strong>Email:</strong> {user?.email}</p>
              <p>
                <strong>Member since:</strong>{' '}
                {user?.date_joined && new Date(user.date_joined).toLocaleDateString('en-PH', {
                  year: 'numeric', month: 'long', day: 'numeric'
                })}
              </p>
              <hr />
              <div className="d-flex gap-2">
                <Link to="/orders" className="btn btn-dark">
                  My Orders
                  {orders?.length > 0 && (
                    <span className="badge bg-light text-dark ms-2">
                      {orders.length}
                    </span>
                  )}
                </Link>
                <button className="btn btn-outline-danger" onClick={logout}>
                  Logout
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}