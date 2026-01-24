import api from "./api";

/* Función para obtener el foro y los canales del backend */
export const getForo = async () => {
  const response = await api.get('/api/v1/foro/');
  return response.data;
};

/* Funcion para obtener los mensajes de un canal */
export const getMensajes = async (id) => {
  const response = await api.get(`api/v1/canales/${id}/mensajes`)
  return response.data;
};

/* Funcion para enviar un mensaje en un canal */
export const enviarMensaje = async (idCanal, data) => {
  const response = await api.post(`api/v1/canales/${idCanal}/mensajes/`, data)
  return response.data
}