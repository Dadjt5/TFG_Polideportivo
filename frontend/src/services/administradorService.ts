import api from "./api";

/* Función para recuperar el administrador con todos sus campos */
export const getAdministrador = async (id: number) => {
  const response = await api.get(`api/v1/administradores/${id}/`)
  return response.data
};

/* Función para cambiar ciertos campos del administrador */
export const modificarAdministrador = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/administradores/${id}/`, data)
  return response.data
};

/* Función para eliminar un administrador */
export const eliminarAdministrador = async (id: number) => {
  const response = await api.patch(`api/v1/administradores/${id}/`)
  return response.data
};

/* Función para obtener la configuracion del sistema */
export const getConfiguracion = async () => {
  const response = await api.get(`api/v1/configuracion/`)
  return response.data
};

/* Función para editar la configuracion del sistema */
export const editarConfiguracion = async (data: any) => {
  const response = await api.patch(`api/v1/configuracion/`, data)
  return response.data
};