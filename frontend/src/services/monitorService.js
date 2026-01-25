import api from "./api";

/* Función para recuperar el usuario final con todos sus campos */
export const getMonitor = async (id) => {
  const response = await api.get(`api/v1/monitores/${id}/`)
  return response.data
};

/* Función para obtener las sesiones semanales del monitor */
export const getSesionesSemanales = async (id) => {
  const response = await api.get(`api/v1/monitores/${id}/sesiones/`)
  return response.data
}
