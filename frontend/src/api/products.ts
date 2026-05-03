import api from './axios'
import type { Product, ProductList, Category, ProductParams } from '../types'

export const getProducts = (params?: ProductParams): Promise<ProductList[]> =>
  api.get('/products/', { params }).then(res => res.data)

export const getProduct = (slug: string): Promise<Product> =>
  api.get(`/products/${slug}/`).then(res => res.data)

export const getCategories = (): Promise<Category[]> =>
  api.get('/products/categories/').then(res => res.data)