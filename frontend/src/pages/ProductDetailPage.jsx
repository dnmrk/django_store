import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProduct } from '../api/products'
import { useCart } from '../context/CartContext'
import { useState } from 'react'
import { Link } from 'react-router-dom'

export default function ProductDetailPage() {
  const { slug } = useParams()
  const { addToCart, loading } = useCart()
  const [quantity, setQuantity] = useState(1)
  const [added, setAdded] = useState(false)

  const { data: product, isLoading } = useQuery({
    queryKey: ['product', slug],
    queryFn: () => getProduct(slug),
  })

  const handleAddToCart = async () => {
    await addToCart(product.id, quantity)
    setAdded(true)
    setTimeout(() => setAdded(false), 2000)
  }

  if (isLoading) return (
    <div className="text-center py-5">
      <div className="spinner-border" role="status" />
    </div>
  )

  if (!product) return <div className="container mt-4">Product not found.</div>

  return (
    <div className="container mt-4">
      <div className="row">
        <div className="col-md-6">
          {product.image ? (
            <img src={product.image} className="img-fluid rounded" alt={product.name} />
          ) : (
            <div
              className="bg-secondary text-white d-flex align-items-center justify-content-center rounded"
              style={{ height: 300 }}
            >
              No Image
            </div>
          )}
        </div>
        <div className="col-md-6">
          <h2>{product.name}</h2>
          <p className="text-muted">{product.category?.name}</p>
          <h4 className="fw-bold">₱{product.price}</h4>
          <p>{product.description}</p>

          {product.stock > 0 ? (
            <span className="badge bg-success mb-3">
              In Stock ({product.stock} left)
            </span>
          ) : (
            <span className="badge bg-danger mb-3">Out of Stock</span>
          )}

          {product.stock > 0 && (
            <div className="d-flex align-items-center gap-2 mt-2">
              <input
                type="number"
                className="form-control"
                style={{ width: 80 }}
                value={quantity}
                min={1}
                max={product.stock}
                onChange={e => setQuantity(Number(e.target.value))}
              />
              <button
                className={`btn ${added ? 'btn-success' : 'btn-dark'}`}
                onClick={handleAddToCart}
                disabled={loading}
              >
                {added ? '✅ Added!' : 'Add to Cart 🛒'}
              </button>
            </div>
          )}

          <div className="mt-3">
            <Link to="/" className="btn btn-outline-dark">← Back to Products</Link>
          </div>
        </div>
      </div>
    </div>
  )
}