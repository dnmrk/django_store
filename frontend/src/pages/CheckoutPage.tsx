import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useCart } from '../context/CartContext'
import { useAuth } from '../context/AuthContext'
import { createOrder } from '../api/orders'
import type { OrderCreateData, FormErrors } from '../types'

interface FormField {
  name: keyof OrderCreateData
  label: string
  type: string
  placeholder: string
}

export default function CheckoutPage() {
    const { cart, clearCart } = useCart()
    const { user } = useAuth()
    const navigate = useNavigate()
    const [loading, setLoading] = useState<boolean>(false)
    const [errors, setErrors] = useState<FormErrors>({})

    const [form, setForm] = useState<OrderCreateData>({
        full_name: user?.first_name ? `${user.first_name} ${user.last_name}` : '',
        email: user?.email || '',
        address: '',
        city: '',
        postal_code: '',
    })

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value })
        setErrors({ ...errors, [e.target.name]: '' })
    }

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        setLoading(true)
        setErrors({})

        try {
            const order = await createOrder(form)
            await clearCart()
            navigate(`/orders/${order.id}`)
        } catch (err) {
            if (axios.isAxiosError(err) && err.response?.data) {
                setErrors(err.response.data)
            }
        } finally {
            setLoading(false)
        }
    }

    if (!user) {
        return (
            <div className="container mt-4 text-center py-5">
                <h4 className="text-muted">Please log in to checkout.</h4>
                <button
                    className="btn btn-dark mt-3"
                    onClick={() => navigate('/login', { state: { from: '/checkout' } })}
                >
                    Login to Continue
                </button>
            </div>
        )
    }

    if (cart.items.length === 0) {
        return (
            <div className="container mt-4 text-center py-5">
                <h4 className="text-muted">Your cart is empty.</h4>
                <button className="btn btn-dark mt-3" onClick={() => navigate('/')}>
                    Start Shopping
                </button>
            </div>
        )
    }

    const fields: FormField[] = [
        { name: 'full_name', label: 'Full Name', type: 'text', placeholder: 'Juan dela Cruz' },
        { name: 'email', label: 'Email', type: 'email', placeholder: 'juan@email.com' },
        { name: 'address', label: 'Address', type: 'textarea', placeholder: '123 Rizal St, Barangay...' },
        { name: 'city', label: 'City', type: 'text', placeholder: 'Manila' },
        { name: 'postal_code', label: 'Postal Code', type: 'text', placeholder: '1000' },
    ]

    return (
        <div className="container mt-4">
            <h2 className="mb-4">Checkout</h2>
            <div className="row">

                {/* Shipping Form */}
                <div className="col-md-7">
                    <div className="card shadow-sm mb-4">
                        <div className="card-body p-4">
                            <h5 className="mb-3">Shipping Details</h5>
                            <form onSubmit={handleSubmit}>
                                {fields.map(field => (
                                    <div className="mb-3" key={field.name}>
                                        <label className="form-label fw-semibold">{field.label}</label>
                                        {field.type === 'textarea' ? (
                                            <textarea
                                                name={field.name}
                                                className={`form-control ${errors[field.name] ? 'is-invalid' : ''}`}
                                                placeholder={field.placeholder}
                                                value={form[field.name]}
                                                onChange={handleChange}
                                                rows={3}
                                            />
                                        ) : (
                                            <input
                                                type={field.type}
                                                name={field.name}
                                                className={`form-control ${errors[field.name] ? 'is-invalid' : ''}`}
                                                placeholder={field.placeholder}
                                                value={form[field.name]}
                                                onChange={handleChange}
                                            />
                                        )}
                                        {errors[field.name] && (
                                            <div className="invalid-feedback">{errors[field.name]}</div>
                                        )}
                                    </div>
                                ))}
                                <button
                                    type="submit"
                                    className="btn btn-dark w-100 mt-2"
                                    disabled={loading}
                                >
                                    {loading ? (
                                        <>
                                            <span className="spinner-border spinner-border-sm me-2" />
                                            Placing Order...
                                        </>
                                    ) : (
                                        'Place Order ✅'
                                    )}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>

                {/* Order Summary */}
                <div className="col-md-5">
                    <div className="card shadow-sm">
                        <div className="card-body p-4">
                            <h5 className="mb-3">Order Summary</h5>
                            <ul className="list-group list-group-flush">
                                {cart.items.map(item => (
                                    <li
                                        key={item.product.id}
                                        className="list-group-item d-flex justify-content-between px-0"
                                    >
                                        <span>{item.product.name} x{item.quantity}</span>
                                        <span>₱{item.total_price.toFixed(2)}</span>
                                    </li>
                                ))}
                            </ul>
                            <hr />
                            <div className="d-flex justify-content-between fw-bold fs-5">
                                <span>Total</span>
                                <span>₱{Number(cart.total_price).toFixed(2)}</span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    )
}