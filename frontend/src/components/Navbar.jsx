import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useCart } from '../context/CartContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const { cart } = useCart()

  return (
    <nav className="navbar navbar-dark bg-dark px-4">
      <Link className="navbar-brand" to="/">🛒 Django Store</Link>
      <div className="d-flex gap-3 align-items-center">

        <Link to="/cart" className="text-white text-decoration-none">
          🛒 Cart
          {cart.total_items > 0 && (
            <span className="badge bg-warning text-dark ms-1">
              {cart.total_items}
            </span>
          )}
        </Link>

        {user ? (
          <>
            <Link to="/profile" className="text-white text-decoration-none">
              👤 {user.username}
            </Link>
            <button
              className="btn btn-outline-light btn-sm"
              onClick={logout}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="btn btn-outline-light btn-sm">Login</Link>
            <Link to="/register" className="btn btn-light btn-sm">Register</Link>
          </>
        )}
      </div>
    </nav>
  )
}