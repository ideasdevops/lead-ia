import api from './client'

export interface SearchQuery {
  id: number
  user_id: number
  query: string
  location: string
  source: 'google_maps' | 'yelp'
  zoom?: number
  status: 'pending' | 'running' | 'completed' | 'failed'
  created_at: string
  completed_at?: string
  leads_count: number
  leads?: Lead[]
}

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

export const searchApi = {
  start: async (data: {
    query: string
    location: string
    source: 'google_maps' | 'yelp'
    zoom?: number
  }): Promise<{ message: string; search_query: SearchQuery }> => {
    const response = await api.post('/search/start', data)
    return response.data
  },

  execute: async (searchId: number): Promise<{
    message: string
    search_query: SearchQuery
    leads_count: number
  }> => {
    const response = await api.post(`/search/execute/${searchId}`)
    return response.data
  },

  list: async (): Promise<{ searches: SearchQuery[] }> => {
    const response = await api.get('/search/list')
    return response.data
  },

  get: async (id: number): Promise<{ search_query: SearchQuery }> => {
    const response = await api.get(`/search/${id}`)
    return response.data
  },
}

