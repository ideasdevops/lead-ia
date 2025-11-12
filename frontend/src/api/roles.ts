import api from './client'

export interface Permission {
  id: number
  name: string
  description: string
  created_at: string
}

export interface Role {
  id: number
  name: string
  description: string
  created_at: string
  permissions: string[]
}

export const rolesApi = {
  list: async (): Promise<{ roles: Role[] }> => {
    const response = await api.get('/roles/list')
    return response.data
  },

  get: async (id: number): Promise<{ role: Role }> => {
    const response = await api.get(`/roles/${id}`)
    return response.data
  },

  create: async (data: {
    name: string
    description?: string
    permissions?: string[]
  }): Promise<{ role: Role }> => {
    const response = await api.post('/roles/create', data)
    return response.data
  },

  update: async (id: number, data: {
    name?: string
    description?: string
    permissions?: string[]
  }): Promise<{ role: Role }> => {
    const response = await api.put(`/roles/${id}`, data)
    return response.data
  },

  delete: async (id: number): Promise<{ message: string }> => {
    const response = await api.delete(`/roles/${id}`)
    return response.data
  },

  listPermissions: async (): Promise<{ permissions: Permission[] }> => {
    const response = await api.get('/roles/permissions')
    return response.data
  },
}

