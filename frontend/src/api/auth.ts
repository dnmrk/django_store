import api from './axios'
import type { User, RegisterData, LoginData, LoginResponse, AuthTokens } from '../types'

export const registerUser = (data: RegisterData): Promise<LoginResponse> =>
  api.post('/auth/register/', data).then(res => res.data)

export const loginUser = async (data: LoginData): Promise<LoginResponse> => {
  const tokens = await api.post<AuthTokens>('/auth/login/', data).then(res => res.data)
  localStorage.setItem('access_token', tokens.access)
  localStorage.setItem('refresh_token', tokens.refresh)
  const user = await api.get<User>('/auth/profile/').then(res => res.data)
  return { ...tokens, user }
}

export const getProfile = (): Promise<User> =>
  api.get('/auth/profile/').then(res => res.data)