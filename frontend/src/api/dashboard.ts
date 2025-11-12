import api from './client'

export interface DashboardStats {
  total_searches: number
  total_leads: number
  total_users: number
  searches_by_status: Record<string, number>
  leads_by_source: Record<string, number>
  recent_searches: number
  recent_leads: number
  searches_by_month: Array<{ month: string; count: number }>
}

export const dashboardApi = {
  getStats: async (): Promise<DashboardStats> => {
    const response = await api.get('/dashboard/stats')
    return response.data
  },
}

