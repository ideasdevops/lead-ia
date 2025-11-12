import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { leadsApi } from '../api/leads'
import { searchApi } from '../api/search'
import { Download, Filter, X } from 'lucide-react'
import toast from 'react-hot-toast'

const Results = () => {
  const [filters, setFilters] = useState({
    search_query_id: '',
    source: '',
    page: 1,
    per_page: 50,
  })

  const { data: searches } = useQuery({
    queryKey: ['searches'],
    queryFn: () => searchApi.list(),
  })

  const { data: leadsData, isLoading } = useQuery({
    queryKey: ['leads', filters],
    queryFn: () =>
      leadsApi.list({
        search_query_id: filters.search_query_id
          ? parseInt(filters.search_query_id)
          : undefined,
        source: filters.source || undefined,
        page: filters.page,
        per_page: filters.per_page,
      }),
  })

  const handleExport = async () => {
    try {
      const blob = await leadsApi.export({
        search_query_id: filters.search_query_id
          ? parseInt(filters.search_query_id)
          : undefined,
        source: filters.source || undefined,
      })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'leads.csv'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
      toast.success('Leads exportados exitosamente')
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Error al exportar leads')
    }
  }

  const clearFilters = () => {
    setFilters({
      search_query_id: '',
      source: '',
      page: 1,
      per_page: 50,
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Resultados de Leads</h1>
          <p className="mt-2 text-sm text-gray-600">
            Visualiza y filtra los leads obtenidos de las búsquedas
          </p>
        </div>
        <button
          onClick={handleExport}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
        >
          <Download className="h-5 w-5 mr-2" />
          Exportar CSV
        </button>
      </div>

      {/* Filtros */}
      <div className="bg-white shadow rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-medium text-gray-900 flex items-center">
            <Filter className="h-5 w-5 mr-2" />
            Filtros
          </h2>
          {(filters.search_query_id || filters.source) && (
            <button
              onClick={clearFilters}
              className="text-sm text-primary-600 hover:text-primary-700 flex items-center"
            >
              <X className="h-4 w-4 mr-1" />
              Limpiar
            </button>
          )}
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <div>
            <label htmlFor="search_query" className="block text-sm font-medium text-gray-700">
              Búsqueda
            </label>
            <select
              id="search_query"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              value={filters.search_query_id}
              onChange={(e) =>
                setFilters({ ...filters, search_query_id: e.target.value, page: 1 })
              }
            >
              <option value="">Todas las búsquedas</option>
              {searches?.searches.map((search) => (
                <option key={search.id} value={search.id}>
                  {search.query} - {search.location} ({search.source})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="source" className="block text-sm font-medium text-gray-700">
              Fuente
            </label>
            <select
              id="source"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              value={filters.source}
              onChange={(e) => setFilters({ ...filters, source: e.target.value, page: 1 })}
            >
              <option value="">Todas las fuentes</option>
              <option value="google_maps">Google Maps</option>
              <option value="yelp">Yelp</option>
            </select>
          </div>

          <div>
            <label htmlFor="per_page" className="block text-sm font-medium text-gray-700">
              Por página
            </label>
            <select
              id="per_page"
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              value={filters.per_page}
              onChange={(e) =>
                setFilters({ ...filters, per_page: parseInt(e.target.value), page: 1 })
              }
            >
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
        </div>
      </div>

      {/* Tabla de resultados */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Título
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Dirección
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Teléfono
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Sitio Web
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Tags
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {isLoading ? (
                <tr>
                  <td colSpan={5} className="px-6 py-4 text-center">
                    Cargando...
                  </td>
                </tr>
              ) : leadsData?.leads.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-4 text-center text-gray-500">
                    No se encontraron leads
                  </td>
                </tr>
              ) : (
                leadsData?.leads.map((lead) => (
                  <tr key={lead.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {lead.title || '-'}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">{lead.address || '-'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {lead.phone_number || '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {lead.website_url ? (
                        <a
                          href={lead.website_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary-600 hover:text-primary-900"
                        >
                          {lead.website_url}
                        </a>
                      ) : (
                        '-'
                      )}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">{lead.tags || '-'}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Paginación */}
        {leadsData && leadsData.pages > 1 && (
          <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
            <div className="flex-1 flex justify-between sm:hidden">
              <button
                onClick={() => setFilters({ ...filters, page: filters.page - 1 })}
                disabled={filters.page === 1}
                className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Anterior
              </button>
              <button
                onClick={() => setFilters({ ...filters, page: filters.page + 1 })}
                disabled={filters.page === leadsData.pages}
                className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Siguiente
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Mostrando{' '}
                  <span className="font-medium">
                    {(filters.page - 1) * filters.per_page + 1}
                  </span>{' '}
                  a{' '}
                  <span className="font-medium">
                    {Math.min(filters.page * filters.per_page, leadsData.total)}
                  </span>{' '}
                  de <span className="font-medium">{leadsData.total}</span> resultados
                </p>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                  <button
                    onClick={() => setFilters({ ...filters, page: filters.page - 1 })}
                    disabled={filters.page === 1}
                    className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                  >
                    Anterior
                  </button>
                  <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                    Página {filters.page} de {leadsData.pages}
                  </span>
                  <button
                    onClick={() => setFilters({ ...filters, page: filters.page + 1 })}
                    disabled={filters.page === leadsData.pages}
                    className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                  >
                    Siguiente
                  </button>
                </nav>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Results

