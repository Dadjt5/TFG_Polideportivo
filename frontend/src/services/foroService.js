import api from "./api";

/* Función para obtener el foro y los canales del backend */
export const getForo = async () => {
  const response = await api.get('/api/v1/foro/');
  return response.data;
};
