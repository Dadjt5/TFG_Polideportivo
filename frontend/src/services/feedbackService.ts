import api from "./api";

/* Función para obtener el feedback */
export const getFeedback = async () => {
  const response = await api.get(`api/v1/feedback/`);
  return response.data;
};

/* Función para crear un nuevo feedback */
export const nuevoFeedback = async (tipo: string, mensaje: string, valoracion: any) => {
  const response = await api.post(`api/v1/feedback/`, {tipo: tipo, mensaje: mensaje, valoracion: valoracion})
  return response.data;
};
