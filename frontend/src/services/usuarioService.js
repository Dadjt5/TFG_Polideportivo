import api from "./api";

/* Función para obtener las notificaciones */
export const getNotificaciones = async () => {
  const response = await api.get("api/v1/notificaciones/");
  return response.data;
};
