import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import api from '../api/axios'
import type { Cart } from '../types'

interface CartContextType {
  cart: Cart
  loading: boolean
  fetchCart: () => Promise<void>
  addToCart: (productId: number, quantity?: number) => Promise<void>
  removeFromCart: (productId: number) => Promise<void>
  clearCart: () => Promise<void>
}

const defaultCart: Cart = {
  items: [],
  total_price: 0,
  total_items: 0,
}

const CartContext = createContext<CartContextType | null>(null)

export function CartProvider({ children }: { children: ReactNode }) {
  const [cart, setCart] = useState<Cart>(defaultCart)
  const [loading, setLoading] = useState<boolean>(false)

  const fetchCart = async (): Promise<void> => {
    try {
      const { data } = await api.get<Cart>('/cart/')
      setCart(data)
    } catch {
      console.error('Failed to fetch cart')
    }
  }

  useEffect(() => {
    fetchCart()
  }, [])

  const addToCart = async (productId: number, quantity: number = 1): Promise<void> => {
    setLoading(true)
    try {
      await api.post('/cart/add/', { product_id: productId, quantity })
      await fetchCart()
    } finally {
      setLoading(false)
    }
  }

  const removeFromCart = async (productId: number): Promise<void> => {
    setLoading(true)
    try {
      await api.delete(`/cart/remove/${productId}/`)
      await fetchCart()
    } finally {
      setLoading(false)
    }
  }

  const clearCart = async (): Promise<void> => {
    await api.delete('/cart/clear/')
    await fetchCart()
  }

  return (
    <CartContext.Provider value={{ cart, loading, addToCart, removeFromCart, clearCart, fetchCart }}>
      {children}
    </CartContext.Provider>
  )
}

export function useCart(): CartContextType {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within a CartProvider')
  }
  return context
}