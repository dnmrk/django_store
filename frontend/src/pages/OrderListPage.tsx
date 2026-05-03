import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getOrders } from '../api/orders'

const statusColors = {
    pending: 'warning',
    processing: 'info',
    shipped: 'primary',
    delivered: 'success',
    cancelled: 'danger',
}

export default function OrderListPage() {
    const { data: orders, isLoading } = useQuery({
        queryKey: ['orders'],
        queryFn: getOrders,
    })

    if (isLoading) return (
        <div className="text-center py-5">
            <div className="spinner-border" role="status" />
        </div>
    )

    return (
        <div className="container mt-4">
            <h2 className="mb-4">My Orders</h2>

            {orders?.length === 0 ? (
                <div className="text-center py-5">
                    <h4 className="text-muted">You have no orders yet.</h4>
                    <Link to="/" className="btn btn-dark mt-3">Start Shopping</Link>
                </div>
            ) : (
                <div className="table-responsive">
                    <table className="table align-middle">
                        <thead className="table-dark">
                            <tr>
                                <th>Order #</th>
                                <th>Date</th>
                                <th>Items</th>
                                <th>Total</th>
                                <th>Status</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {orders?.map(order => (
                                <tr key={order.id}>
                                    <td>#{order.id}</td>
                                    <td>{new Date(order.created_at).toLocaleDateString('en-PH', {
                                        year: 'numeric', month: 'short', day: 'numeric'
                                    })}</td>
                                    <td>{order.items.length} item(s)</td>
                                    <td>₱{Number(order.total_price).toFixed(2)}</td>
                                    <td>
                                        <span className={`badge bg-${statusColors[order.status]} text-dark`}>
                                            {order.status_display}
                                        </span>
                                    </td>
                                    <td>
                                        <Link
                                            to={`/orders/${order.id}`}
                                            className="btn btn-sm btn-outline-dark"
                                        >
                                            View
                                        </Link>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    )
}