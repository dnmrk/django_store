import api from './axios'

export const getOrders = () =>
  api.get('/orders/').then(res => res.data)

export const getOrder = (id) =>
  api.get(`/orders/${id}/`).then(res => res.data)

export const createOrder = (data) =>
  api.post('/orders/create/', data).then(res => res.data)