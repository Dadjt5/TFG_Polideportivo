import api from "./api";


/* Función para obtener el foro y los canales del backend */
export const getForo = async () => {
  const response = await api.get('/api/v1/foro/');
  return response.data;
};

/* Funcion para obtener los mensajes de un canal */
export const getMensajes = async (id: number) => {
  const response = await api.get(`api/v1/canales/${id}/mensajes/`)
  return response.data;
};

/* Funcion para enviar un mensaje en un canal */
export const enviarMensaje = async (idCanal: number, data: any) => {
  const response = await api.post(`api/v1/canales/${idCanal}/mensajes/`, data)
  return response.data
}

/* Función para crear un nuevo canal en el foro */
export const nuevoCanal = async (id: number, payload: any) => {
  const response = await api.post(`api/v1/foro/${id}/canales/`, payload)
  return response.data
}

/* Funcion para silenciar o expulsar a un usuario de un canal */
export const modificarUsuarioFinal = async (idCanal: number, idUsuario: number, accion: any) => {
  const response = await api.patch(`api/v1/canales/${idCanal}/modificar/${idUsuario}/`, accion)
  return response.data;
};
