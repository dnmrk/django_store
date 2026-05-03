// ─── Auth ────────────────────────────────────────────────────────────────────

export interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  date_joined: string
}

export interface AuthTokens {
  access: string
  refresh: string
}

export interface LoginResponse extends AuthTokens {
  user: User
}

export interface RegisterData {
  username: string
  email: string
  password: string
  password2: string
}

export interface LoginData {
  username: string
  password: string
}

// ─── Products ────────────────────────────────────────────────────────────────

export interface Category {
  id: number
  name: string
  slug: string
}

export interface Product {
  id: number
  name: string
  slug: string
  description: string
  price: string
  image: string | null
  stock: number
  available: boolean
  category: Category
  created_at: string
}

export interface ProductList {
  id: number
  name: string
  slug: string
  price: string
  image: string | null
  stock: number
  available: boolean
  category_name: string
}

export interface ProductParams {
  search?: string
  category?: string
}

// ─── Cart ────────────────────────────────────────────────────────────────────

export interface CartItem {
  product: ProductList
  quantity: number
  price: string
  total_price: number
}

export interface Cart {
  items: CartItem[]
  total_price: number
  total_items: number
}

// ─── Orders ──────────────────────────────────────────────────────────────────

export type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'

export interface OrderItem {
  id: number
  product: ProductList
  quantity: number
  price: string
  total_price: number
}

export interface Order {
  id: number
  full_name: string
  email: string
  address: string
  city: string
  postal_code: string
  status: OrderStatus
  status_display: string
  items: OrderItem[]
  total_price: number
  created_at: string
}

export interface OrderCreateData {
  full_name: string
  email: string
  address: string
  city: string
  postal_code: string
}

// ─── Forms ───────────────────────────────────────────────────────────────────

export type FormErrors = Record<string, string | string[]>