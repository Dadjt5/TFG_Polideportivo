import api from "./api";

/* Funcion para obtener las estadisticas desde el backend */
export const getEstadisticas = async () => {
  const response = await api.get("estadisticas/");
  return response.data;
};
