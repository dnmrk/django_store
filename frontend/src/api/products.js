import api from './axios'

export const getProducts = (params) =>
  api.get('/products/', { params }).then(res => res.data)

export const getProduct = (slug) =>
  api.get(`/products/${slug}/`).then(res => res.data)

export const getCategories = () =>
  api.get('/products/categories/').then(res => res.data)