import { Link, useNavigate } from 'react-router-dom'
import { useCart } from '../context/CartContext'

export default function CartPage() {
  const { cart, removeFromCart, loading } = useCart()
  const navigate = useNavigate()

  if (cart.items.length === 0) {
    return (
      <div className="container mt-4 text-center py-5">
        <h4 className="text-muted">Your cart is empty.</h4>
        <Link to="/" className="btn btn-dark mt-3">Start Shopping</Link>
      </div>
    )
  }

  return (
    <div className="container mt-4">
      <h2 className="mb-4">🛒 Your Cart</h2>

      <div className="table-responsive">
        <table className="table align-middle">
          <thead className="table-dark">
            <tr>
              <th>Product</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Total</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {cart.items.map(item => (
              <tr key={item.product.id}>
                <td>
                  <Link
                    to={`/products/${item.product.slug}`}
                    className="text-decoration-none text-dark fw-semibold"
                  >
                    {item.product.name}
                  </Link>
                </td>
                <td>₱{item.price}</td>
                <td>{item.quantity}</td>
                <td>₱{item.total_price.toFixed(2)}</td>
                <td>
                  <button
                    className="btn btn-sm btn-outline-danger"
                    onClick={() => removeFromCart(item.product.id)}
                    disabled={loading}
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="text-end mt-3">
        <h4>Total: <strong>₱{Number(cart.total_price).toFixed(2)}</strong></h4>
        <Link to="/" className="btn btn-outline-dark me-2">← Continue Shopping</Link>
        <button
          className="btn btn-dark"
          onClick={() => navigate('/checkout')}
        >
          Proceed to Checkout
        </button>
      </div>
    </div>
  )
}