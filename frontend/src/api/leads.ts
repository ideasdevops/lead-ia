import api from './client'

export interface Lead {
  id: number
  search_query_id: number
  title: string
  address: string
  phone_number: string
  website_url: string
  tags: string
  source_url: string
  created_at: string
}

export interface LeadsResponse {
  leads: Lead[]
  total: number
  pages: number
  current_page: number
}

export const leadsApi = {
  list: async (params?: {
    search_query_id?: number
    source?: string
    page?: number
    per_page?: number
  }): Promise<LeadsResponse> => {
    const response = await api.get('/leads/list', { params })
    return response.data
  },

  get: async (id: number): Promise<{ lead: Lead }> => {
    const response = await api.get(`/leads/${id}`)
    return response.data
  },

  export: async (params?: {
    search_query_id?: number
    source?: string
  }): Promise<Blob> => {
    const response = await api.get('/leads/export', {
      params,
      responseType: 'blob',
    })
    return response.data
  },
}

