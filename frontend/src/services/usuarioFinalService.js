import api from "./api";

/* Función para obtener las notificaciones */
export const getNotificaciones = async () => {
  const response = await api.get("api/v1/notificaciones/");
  return response.data;
};

/* Función para guardar los campos de las notificaciones */
export const guardarNotificaciones = async (payload) => {
  const response = await api.post("api/v1/notificaciones/guardar", payload);
  return response.data;
};

/* Función para borrar notificaciones */
export const borrarNotificaciones = async (id) => {
  await api.delete(`api/v1/notificaciones/${id}/`)
};


/* Función para recuperar el usuario con todos sus campos */
export const getUsuarioFinal = async (id) => {
  const response = await api.get(`api/v1/usuariosFinales/${id}/`)
  return response.data
};
