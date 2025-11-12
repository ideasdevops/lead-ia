import api from './client'

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  is_active: boolean
  is_approved: boolean
  created_at: string
  last_login?: string
  roles: string[]
}

export interface UsersResponse {
  users: User[]
  total: number
  pages: number
  current_page: number
}

export const usersApi = {
  list: async (params?: {
    page?: number
    per_page?: number
    search?: string
  }): Promise<UsersResponse> => {
    const response = await api.get('/users/list', { params })
    return response.data
  },

  get: async (id: number): Promise<{ user: User }> => {
    const response = await api.get(`/users/${id}`)
    return response.data
  },

  update: async (id: number, data: Partial<User> & { password?: string; roles?: string[] }): Promise<{ user: User }> => {
    const response = await api.put(`/users/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete(`/users/${id}`)
    return response.data
  },

  approve: async (id: number): Promise<{ message: string; user: User }> => {
    const response = await api.post(`/users/${id}/approve`)
    return response.data
  },

  listPending: async (): Promise<{ users: User[] }> => {
    const response = await api.get('/users/pending')
    return response.data
  },
}

