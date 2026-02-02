import api from "./api";

/* Función para obtener la tarifa y descuentos de una actividad */
export const getTarifaDescuentoActividad = async (id) => {
  const response = await api.get(`api/v1/tarifas/actividades/${id}/`)
  return response.data;
}

/* Función para obtener la tarifa y descuentos de una instalacion */
export const getTarifaDescuentoInstalacion = async (id, fecha) => {
  const response = await api.get(`api/v1/tarifas/instalaciones/${id}/`, {
    params: { fecha }  // aquí mandamos la fecha como query param
  });
  return response.data;
}

/* Funcion para obtener información de una reserva de una actividad */
export const getReservaActividad = async (id) => {
  const response = await api.get(`api/v1/reservasActividad/${id}/`)
  return response.data;
};
