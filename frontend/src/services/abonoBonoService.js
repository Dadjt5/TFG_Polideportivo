import api from "./api";

/* Función para obtener los abonos */
export const getAbonos = async () => {
  const response = await api.get('/api/v1/abonos/');
  return response.data;
};

/* Función para obtener los abonos */
export const getBonos = async () => {
  const response = await api.get('/api/v1/bonos/');
  return response.data;
};
