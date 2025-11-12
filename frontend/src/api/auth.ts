import api from './client'

export interface LoginData {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  first_name?: string
  last_name?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
}

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  is_active: boolean
  is_approved: boolean
  roles: string[]
}

export const authApi = {
  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', data)
    return response.data
  },

  register: async (data: RegisterData): Promise<{ message: string; user: User }> => {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  getCurrentUser: async (): Promise<{ user: User }> => {
    const response = await api.get('/auth/me')
    return response.data
  },

  refreshToken: async (): Promise<{ access_token: string }> => {
    const response = await api.post('/auth/refresh')
    return response.data
  },
}

