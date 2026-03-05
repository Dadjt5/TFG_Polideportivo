import api from "./api";

/* Función para cancelar un bono */
export const cancelarBono = async (id: number) => {
  const response = await api.delete(`api/v1/bonos/${id}/cancelar/`)
  return response.data;
}

/* Función para cancelar un abono */
export const cancelarAbono = async (id: number) => {
  const response = await api.delete(`api/v1/abonos/${id}/cancelar/`)
  return response.data;
}

/* Función para cancelar una reserva de una actividad */
export const cancelarReservaActividad = async (id: number) => {
  const response = await api.delete(`api/v1/reservas/${id}/cancelar/`)
  return response.data;
}

/* Función para cancelar un alquiler */
export const cancelarAlquiler = async (id: number) => {
  const response = await api.delete(`api/v1/alquileres/${id}/cancelar/`)
  return response.data;
}
