import { useParams, Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getOrder } from '../api/orders'

const statusColors = {
    pending: 'warning',
    processing: 'info',
    shipped: 'primary',
    delivered: 'success',
    cancelled: 'danger',
}

export default function OrderDetailPage() {
    const { id } = useParams()

    const { data: order, isLoading } = useQuery({
        queryKey: ['order', id],
        queryFn: () => getOrder(id),
    })

    if (isLoading) return (
        <div className="text-center py-5">
            <div className="spinner-border" role="status" />
        </div>
    )

    if (!order) return (
        <div className="container mt-4">Order not found.</div>
    )

    return (
        <div className="container mt-4">
            <div className="row justify-content-center">
                <div className="col-md-8">

                    <div className="alert alert-success">
                        ✅ <strong>Order placed successfully!</strong> Your order
                        <strong> #{order.id}</strong> is now{' '}
                        <span className={`badge bg-${statusColors[order.status]}`}>
                            {order.status_display}
                        </span>
                    </div>

                    {/* Shipping Details */}
                    <div className="card shadow-sm mb-4">
                        <div className="card-body p-4">
                            <h5 className="mb-3">Shipping Details</h5>
                            <p><strong>Name:</strong> {order.full_name}</p>
                            <p><strong>Email:</strong> {order.email}</p>
                            <p><strong>Address:</strong> {order.address}</p>
                            <p><strong>City:</strong> {order.city}</p>
                            <p><strong>Postal Code:</strong> {order.postal_code}</p>
                        </div>
                    </div>

                    {/* Order Items */}
                    <div className="card shadow-sm mb-4">
                        <div className="card-body p-4">
                            <h5 className="mb-3">Items Ordered</h5>
                            <ul className="list-group list-group-flush">
                                {order.items.map(item => (
                                    <li
                                        key={item.id}
                                        className="list-group-item d-flex justify-content-between px-0"
                                    >
                                        <span>{item.product.name} x{item.quantity}</span>
                                        <span>₱{Number(item.total_price).toFixed(2)}</span>
                                    </li>
                                ))}
                            </ul>
                            <hr />
                            <div className="d-flex justify-content-between fw-bold fs-5">
                                <span>Total</span>
                                <span>₱{Number(order.total_price).toFixed(2)}</span>
                            </div>
                        </div>
                    </div>

                    <div className="d-flex gap-2">
                        <Link to="/orders" className="btn btn-outline-dark">My Orders</Link>
                        <Link to="/" className="btn btn-dark">Continue Shopping</Link>
                    </div>

                </div>
            </div>
        </div>
    )
}