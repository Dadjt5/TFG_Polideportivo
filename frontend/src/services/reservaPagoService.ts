import api from "./api";

/* Función para obtener la tarifa y descuentos de una actividad */
export const getTarifaDescuentoActividad = async (id: number) => {
  const response = await api.get(`api/v1/tarifas/actividades/${id}/`)
  return response.data;
}

/* Función para obtener la tarifa y descuentos de una instalacion */
export const getTarifaDescuentoInstalacion = async (id: number, fecha: string) => {
  const response = await api.get(`api/v1/tarifas/instalaciones/${id}/`, {
    params: { fecha }
  });
  return response.data;
}

/* Funcion para obtener información de una reserva de una actividad */
export const getReservaActividad = async (id: number) => {
  const response = await api.get(`api/v1/reservasActividad/${id}/`)
  return response.data;
};

/* Funcion para obtener información de una reserva de una actividad, pero solo ciertos datos */
export const getReservaActividadSimplificado = async (id: number) => {
  const response = await api.get(`api/v1/reservasActividadSimple/${id}/`)
  return response.data;
};

/* Funcion para obtener información de un alquiler de una instalacion */
export const getAlquiler = async (id: number) => {
  const response = await api.get(`api/v1/alquileres/${id}/`)
  return response.data;
};

/* Funcion para obtener información de un alquiler de una instalacion, pero solo ciertos datos */
export const getAlquilerSimplificado = async (id: number) => {
  const response = await api.get(`api/v1/alquileresSimple/${id}/`)
  return response.data;
};

/* Función para reservar la actividad */
export const reservarActividad = async(id: number) => {
  const response = await api.post(`api/v1/actividades/${id}/reservar/`)
  return response.data;
}

/* Función para intentar lanzar un pago */
export const intentarPago = async(id: number) => {
  const response = await api.post("api/v1/pago/comenzar/", {reserva_id: id})
  return response.data;
}

/* Función para confirmar un pago */
export const confirmarPago = async(id: number) => {
  const response = await api.post("api/v1/pago/confirmar/", {reserva_id: id})
  return response.data;
}