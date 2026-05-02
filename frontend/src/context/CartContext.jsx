import { createContext, useContext, useState, useEffect } from 'react'
import api from '../api/axios'

const CartContext = createContext()

export function CartProvider({ children }) {
    const [cart, setCart] = useState({ items: [], total_price: 0, total_items: 0 })
    const [loading, setLoading] = useState(false)

    const fetchCart = async () => {
        try {
            const { data } = await api.get('/cart/')
            setCart(data)
        } catch {
            console.error('Failed to fetch cart')
        }
    }

    useEffect(() => {
        fetchCart()
    }, [])

    const addToCart = async (productId, quantity = 1) => {
        setLoading(true)
        try {
            await api.post('/cart/add/', { product_id: productId, quantity })
            await fetchCart()
        } finally {
            setLoading(false)
        }
    }

    const removeFromCart = async (productId) => {
        setLoading(true)
        try {
            await api.delete(`/cart/remove/${productId}/`)
            await fetchCart()
        } finally {
            setLoading(false)
        }
    }

    const clearCart = async () => {
        await api.delete('/cart/clear/')
        await fetchCart()
    }

    return (
    <CartContext.Provider value={{ cart, loading, addToCart, removeFromCart, clearCart, fetchCart }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart() {
    return useContext(CartContext)
}