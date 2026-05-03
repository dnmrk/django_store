import api from './axios'
import type { Order, OrderCreateData } from '../types'

export const getOrders = (): Promise<Order[]> =>
  api.get('/orders/').then(res => res.data)

export const getOrder = (id: string | number): Promise<Order> =>
  api.get(`/orders/${id}/`).then(res => res.data)

export const createOrder = (data: OrderCreateData): Promise<Order> =>
  api.post('/orders/create/', data).then(res => res.data)