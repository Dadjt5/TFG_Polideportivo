import api from "./api";

/* Función para recuperar el administrador con todos sus campos */
export const getAdministrador = async (id) => {
  const response = await api.get(`api/v1/administradores/${id}/`)
  return response.data
};

/* Función para cambiar ciertos campos del administrador */
export const modificarAdministrador = async (id, data) => {
  const response = await api.patch(`api/v1/administradores/${id}/`, data)
  return response.data
}