import api from "./api";

/* Funcion para obtener información de una reserva de una actividad */
export const getReservaActividad = async (id) => {
  const response = await api.get(`api/v1/reservasActividad/${id}/`)
  return response.data;
};
