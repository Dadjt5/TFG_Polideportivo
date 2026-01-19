import api from "./api";

/* Función para recuperar el usuario final con todos sus campos */
export const getUsuarioFinal = async (id) => {
  const response = await api.get(`api/v1/usuariosFinales/${id}/`)
  return response.data
};


/* Función para obtener las notificaciones */
export const getNotificaciones = async () => {
  const response = await api.get("api/v1/notificaciones/");
  return response.data;
};

/* Función para guardar los campos de las notificaciones */
export const guardarNotificaciones = async (payload) => {
  const response = await api.post("api/v1/notificaciones/guardar/", payload);
  return response.data;
};

/* Función para borrar notificaciones */
export const borrarNotificaciones = async (id) => {
  await api.delete(`api/v1/notificaciones/${id}/`)
};


/* Función para recuperar la TDA */
export const getTDA = async () => {
  const response = await api.get('api/v1/tdas/')
  return response.data
};

/* Función para asignar un usuario a la TDA */
export const validarTDA = async (payload) => {
  const response = await api.post('api/v1/tda/validar/', payload)
  return response.data
};


/* Función para marcar actividades o instalaciones como favoritas */
export const marcarFavoritos = async (payload) => {
  const response = await api.post('api/v1/marcar/favoritas/', payload)
  return response.data
};