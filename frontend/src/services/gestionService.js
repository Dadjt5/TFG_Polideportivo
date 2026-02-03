import api from "./api";

/* Función para obtener los usuarios del sistema */
export const getUsuarios = async () => {
  const response = await api.get('api/v1/usuarios/')
  return response.data;
}