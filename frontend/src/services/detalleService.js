import api from "./api";

/* Función para obtener la informacion de una actividad */
export const getActividadDetalle = async (id) => {
  const response = await api.get(`/api/v1/actividades/${id}/`);
  return response.data;
};

/* Función para obtener la informacion de una instalacion */
export const getInstalacionDetalle = async (id) => {
  const response = await api.get(`/api/v1/instalaciones/${id}/`);
  return response.data;
};

/* Función para obtener la informacion de instalaciones y actividades indicadas */
export const getActividadesInstalaciones = async (payload) => {
  const response = await api.post('/api/v1/obtener/favoritas/', payload);
  return response.data
}