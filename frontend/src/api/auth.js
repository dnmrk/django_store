import api from './axios'

export const registerUser = (data) =>
  api.post('/auth/register/', data).then(res => res.data)

export const loginUser = async (data) => {
  const tokens = await api.post('/auth/login/', data).then(res => res.data)
  // store tokens immediately so the next call has auth
  localStorage.setItem('access_token', tokens.access)
  localStorage.setItem('refresh_token', tokens.refresh)
  const user = await api.get('/auth/profile/').then(res => res.data)
  return { ...tokens, user }
}

export const getProfile = () =>
  api.get('/auth/profile/').then(res => res.data)