import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import api from '../api/axios'
import type { User, AuthTokens } from '../types'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (userData: User, tokens: AuthTokens) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      api.get<User>('/auth/profile/')
        .then(res => setUser(res.data))
        .catch(() => setUser(null))
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = (userData: User, tokens: AuthTokens): void => {
    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('refresh_token', tokens.refresh)
    setUser(userData)
  }

  const logout = (): void => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}