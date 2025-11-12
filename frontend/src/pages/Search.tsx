import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { searchApi } from '../api/search'
import { Search as SearchIcon, Play, Loader } from 'lucide-react'
import toast from 'react-hot-toast'

const Search = () => {
  const [formData, setFormData] = useState({
    query: '',
    location: '',
    source: 'google_maps' as 'google_maps' | 'yelp',
    zoom: 12,
  })

  const queryClient = useQueryClient()

  const { data: searches, isLoading } = useQuery({
    queryKey: ['searches'],
    queryFn: () => searchApi.list(),
  })

  const startMutation = useMutation({
    mutationFn: searchApi.start,
    onSuccess: () => {
      toast.success('Búsqueda iniciada')
      queryClient.invalidateQueries({ queryKey: ['searches'] })
      setFormData({ query: '', location: '', source: 'google_maps', zoom: 12 })
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Error al iniciar búsqueda')
    },
  })

  const executeMutation = useMutation({
    mutationFn: searchApi.execute,
    onSuccess: () => {
      toast.success('Búsqueda ejecutada exitosamente')
      queryClient.invalidateQueries({ queryKey: ['searches'] })
      queryClient.invalidateQueries({ queryKey: ['leads'] })
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Error al ejecutar búsqueda')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    startMutation.mutate({
      query: formData.query,
      location: formData.location,
      source: formData.source,
      zoom: formData.source === 'google_maps' ? formData.zoom : undefined,
    })
  }

  const handleExecute = (searchId: number) => {
    if (confirm('¿Ejecutar esta búsqueda ahora?')) {
      executeMutation.mutate(searchId)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'running':
        return 'bg-blue-100 text-blue-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-yellow-100 text-yellow-800'
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Búsqueda y Prospección</h1>
        <p className="mt-2 text-sm text-gray-600">
          Inicia nuevas búsquedas de leads en Google Maps o Yelp
        </p>
      </div>

      {/* Formulario de búsqueda */}
      <div className="bg-white shadow rounded-lg p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="query" className="block text-sm font-medium text-gray-700">
                Palabra Clave
              </label>
              <input
                type="text"
                id="query"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                placeholder="Ej: Barbershop, Pizza, Gym"
                value={formData.query}
                onChange={(e) => setFormData({ ...formData, query: e.target.value })}
              />
            </div>

            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                Ubicación
              </label>
              <input
                type="text"
                id="location"
                required
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                placeholder="Ej: Paris, Madrid, New York"
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="source" className="block text-sm font-medium text-gray-700">
                Fuente
              </label>
              <select
                id="source"
                className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                value={formData.source}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    source: e.target.value as 'google_maps' | 'yelp',
                  })
                }
              >
                <option value="google_maps">Google Maps</option>
                <option value="yelp">Yelp</option>
              </select>
            </div>

            {formData.source === 'google_maps' && (
              <div>
                <label htmlFor="zoom" className="block text-sm font-medium text-gray-700">
                  Zoom (Google Maps)
                </label>
                <input
                  type="number"
                  id="zoom"
                  min="1"
                  max="20"
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                  value={formData.zoom}
                  onChange={(e) =>
                    setFormData({ ...formData, zoom: parseFloat(e.target.value) })
                  }
                />
              </div>
            )}
          </div>

          <div>
            <button
              type="submit"
              disabled={startMutation.isPending}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
            >
              <SearchIcon className="h-5 w-5 mr-2" />
              {startMutation.isPending ? 'Iniciando...' : 'Iniciar Búsqueda'}
            </button>
          </div>
        </form>
      </div>

      {/* Lista de búsquedas */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">Búsquedas Realizadas</h2>
        </div>
        {isLoading ? (
          <div className="p-6 text-center">
            <Loader className="h-6 w-6 animate-spin mx-auto text-primary-600" />
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Query
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ubicación
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fuente
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Estado
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Leads
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Acciones
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {searches?.searches.map((search) => (
                  <tr key={search.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {search.query}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {search.location}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {search.source === 'google_maps' ? 'Google Maps' : 'Yelp'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(
                          search.status
                        )}`}
                      >
                        {search.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {search.leads_count}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      {search.status === 'pending' && (
                        <button
                          onClick={() => handleExecute(search.id)}
                          disabled={executeMutation.isPending}
                          className="text-primary-600 hover:text-primary-900 inline-flex items-center"
                        >
                          <Play className="h-4 w-4 mr-1" />
                          Ejecutar
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default Search

