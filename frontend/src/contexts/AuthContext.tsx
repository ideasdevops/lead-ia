import React, { createContext, useContext, useState, useEffect } from 'react'
import { authApi, User } from '../api/auth'
import toast from 'react-hot-toast'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, first_name?: string, last_name?: string) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      refreshUser()
    } else {
      setLoading(false)
    }
  }, [])

  const refreshUser = async () => {
    try {
      const { user } = await authApi.getCurrentUser()
      setUser(user)
    } catch (error) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      const { access_token, refresh_token, user } = await authApi.login({ email, password })
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
      setUser(user)
      toast.success('Inicio de sesión exitoso')
    } catch (error: any) {
      const message = error.response?.data?.error || 'Error al iniciar sesión'
      toast.error(message)
      throw error
    }
  }

  const register = async (email: string, password: string, first_name?: string, last_name?: string) => {
    try {
      const { user } = await authApi.register({ email, password, first_name, last_name })
      toast.success('Registro exitoso. Pendiente de aprobación del administrador.')
    } catch (error: any) {
      const message = error.response?.data?.error || 'Error al registrarse'
      toast.error(message)
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
    toast.success('Sesión cerrada')
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth debe ser usado dentro de AuthProvider')
  }
  return context
}

