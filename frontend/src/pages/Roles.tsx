import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { rolesApi } from '../api'
import { Plus, Edit, Trash2, Shield } from 'lucide-react'
import toast from 'react-hot-toast'

const Roles = () => {
  const [showModal, setShowModal] = useState(false)
  const [editingRole, setEditingRole] = useState<any>(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    permissions: [] as string[],
  })

  const queryClient = useQueryClient()

  const { data: rolesData, isLoading } = useQuery({
    queryKey: ['roles'],
    queryFn: () => rolesApi.list(),
  })

  const { data: permissionsData } = useQuery({
    queryKey: ['permissions'],
    queryFn: () => rolesApi.listPermissions(),
  })

  const createMutation = useMutation({
    mutationFn: rolesApi.create,
    onSuccess: () => {
      toast.success('Rol creado exitosamente')
      queryClient.invalidateQueries({ queryKey: ['roles'] })
      setShowModal(false)
      setFormData({ name: '', description: '', permissions: [] })
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Error al crear rol')
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => rolesApi.update(id, data),
    onSuccess: () => {
      toast.success('Rol actualizado exitosamente')
      queryClient.invalidateQueries({ queryKey: ['roles'] })
      setShowModal(false)
      setEditingRole(null)
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Error al actualizar rol')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: rolesApi.delete,
    onSuccess: () => {
      toast.success('Rol eliminado exitosamente')
      queryClient.invalidateQueries({ queryKey: ['roles'] })
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.error || 'Error al eliminar rol')
    },
  })

  const handleCreate = () => {
    setEditingRole(null)
    setFormData({ name: '', description: '', permissions: [] })
    setShowModal(true)
  }

  const handleEdit = (role: any) => {
    setEditingRole(role)
    setFormData({
      name: role.name,
      description: role.description || '',
      permissions: role.permissions || [],
    })
    setShowModal(true)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (editingRole) {
      updateMutation.mutate({
        id: editingRole.id,
        data: formData,
      })
    } else {
      createMutation.mutate(formData)
    }
  }

  const handleDelete = (id: number, name: string) => {
    if (confirm(`¿Estás seguro de eliminar el rol "${name}"?`)) {
      deleteMutation.mutate(id)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Gestión de Roles y Permisos</h1>
          <p className="mt-2 text-sm text-gray-600">
            Crea y administra roles con permisos específicos
          </p>
        </div>
        <button
          onClick={handleCreate}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
        >
          <Plus className="h-5 w-5 mr-2" />
          Nuevo Rol
        </button>
      </div>

      {/* Lista de roles */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        {isLoading ? (
          <div className="col-span-full text-center py-8">Cargando...</div>
        ) : rolesData?.roles.length === 0 ? (
          <div className="col-span-full text-center py-8 text-gray-500">
            No hay roles creados
          </div>
        ) : (
          rolesData?.roles.map((role) => (
            <div key={role.id} className="bg-white shadow rounded-lg p-6">
              <div className="flex items-start justify-between">
                <div className="flex items-center">
                  <Shield className="h-6 w-6 text-primary-600 mr-2" />
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">{role.name}</h3>
                    {role.description && (
                      <p className="text-sm text-gray-500 mt-1">{role.description}</p>
                    )}
                  </div>
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleEdit(role)}
                    className="text-primary-600 hover:text-primary-900"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  {role.name !== 'superadmin' && (
                    <button
                      onClick={() => handleDelete(role.id, role.name)}
                      className="text-red-600 hover:text-red-900"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  )}
                </div>
              </div>
              <div className="mt-4">
                <p className="text-xs font-medium text-gray-500 uppercase mb-2">Permisos</p>
                <div className="flex flex-wrap gap-1">
                  {role.permissions.length > 0 ? (
                    role.permissions.map((perm) => (
                      <span
                        key={perm}
                        className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800"
                      >
                        {perm}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-gray-400">Sin permisos</span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Modal de creación/edición */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">
                {editingRole ? 'Editar Rol' : 'Nuevo Rol'}
              </h3>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Nombre</label>
                  <input
                    type="text"
                    required
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    disabled={editingRole?.name === 'superadmin'}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Descripción
                  </label>
                  <textarea
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                    rows={3}
                    value={formData.description}
                    onChange={(e) =>
                      setFormData({ ...formData, description: e.target.value })
                    }
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Permisos
                  </label>
                  <div className="space-y-2 max-h-60 overflow-y-auto border rounded-md p-2">
                    {permissionsData?.permissions.map((perm) => (
                      <label key={perm.id} className="flex items-center">
                        <input
                          type="checkbox"
                          className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                          checked={formData.permissions.includes(perm.name)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setFormData({
                                ...formData,
                                permissions: [...formData.permissions, perm.name],
                              })
                            } else {
                              setFormData({
                                ...formData,
                                permissions: formData.permissions.filter(
                                  (p) => p !== perm.name
                                ),
                              })
                            }
                          }}
                        />
                        <span className="ml-2 text-sm text-gray-700">{perm.name}</span>
                        {perm.description && (
                          <span className="ml-2 text-xs text-gray-500">
                            - {perm.description}
                          </span>
                        )}
                      </label>
                    ))}
                  </div>
                </div>
                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={() => {
                      setShowModal(false)
                      setEditingRole(null)
                    }}
                    className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    disabled={createMutation.isPending || updateMutation.isPending}
                    className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
                  >
                    {editingRole ? 'Actualizar' : 'Crear'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Roles

