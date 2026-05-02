import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getProducts, getCategories } from '../api/products'

export default function ProductListPage() {
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')

  const { data: products, isLoading } = useQuery({
    queryKey: ['products', search, category],
    queryFn: () => getProducts({ search, category }),
  })

  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
  })

  return (
    <div className="container mt-4">
      {/* Search & Filter */}
      <div className="row mb-4 g-2">
        <div className="col-md-6">
          <input
            type="text"
            className="form-control"
            placeholder="Search products..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
        <div className="col-md-4">
          <select
            className="form-select"
            value={category}
            onChange={e => setCategory(e.target.value)}
          >
            <option value="">All Categories</option>
            {categories?.map(cat => (
              <option key={cat.id} value={cat.slug}>{cat.name}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Products Grid */}
      {isLoading ? (
        <div className="text-center py-5">
          <div className="spinner-border" role="status" />
        </div>
      ) : (
        <div className="row row-cols-1 row-cols-md-3 g-4">
          {products?.map(product => (
            <div className="col" key={product.id}>
              <div className="card h-100">
                {product.image ? (
                  <img
                    src={product.image}
                    className="card-img-top"
                    alt={product.name}
                    style={{ height: 200, objectFit: 'cover' }}
                  />
                ) : (
                  <div
                    className="bg-secondary text-white d-flex align-items-center justify-content-center"
                    style={{ height: 200 }}
                  >
                    No Image
                  </div>
                )}
                <div className="card-body">
                  <h5 className="card-title">{product.name}</h5>
                  <p className="card-text text-muted">{product.category_name}</p>
                  <p className="card-text fw-bold">₱{product.price}</p>
                  <Link to={`/products/${product.slug}`} className="btn btn-dark">
                    View Product
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}