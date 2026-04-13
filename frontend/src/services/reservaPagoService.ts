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

/* Funcion para obtener información de un alquiler de una instalacion */
export const getAlquiler = async (id: number) => {
  const response = await api.get(`api/v1/alquileres/${id}/`)
  return response.data;
};


/* Función para reservar la actividad */
export const reservarActividad = async(id: number, personas: number, modalidad: string, tipoSesion: string) => {
  const response = await api.post(`api/v1/actividades/${id}/reservar/`, {"complementos": {"personas": personas, "forma": modalidad, "tipoSesion": tipoSesion}})
  return response.data;
}

/* Funcion para pasar a la lista de espera */
export const pasarAListaEspera = async (id: number) => {
  const response = await api.post(`api/v1/actividades/${id}/esperar/`)
  return response.data.posicion;
}

/* Función para alquilar una instalacion */
export const alquilar = async(id: number, complementos: any) => {
  const response = await api.post(`api/v1/instalaciones/${id}/alquilar/`, complementos)
  return response.data;
}

/* Función para comprar un abono */
export const comprarAbono = async(id: number, tipo: string, forma: string, familiar: boolean) => {
  const response = await api.post(`api/v1/abonos/${id}/comprar/`, {"tipoAbono": tipo, "complementos": {"forma": forma, "familiar": familiar}})
  return response.data;
}

/* Función para comprar un bono */
export const comprarBono = async(id: number) => {
  const response = await api.post(`api/v1/bonos/${id}/comprar/`)
  return response.data;
}

export const getPago = async (id: number) => {
  const response = await api.get(`api/v1/pagos/${id}/`)
  return response.data;
}

export const getResumenPago = async (id: number, tipo: string) => {
  const response = await api.get(`api/v1/pagos/resumen/${tipo}/${id}/`)
  return response.data
}

/* Función para intentar lanzar un pago */
export const intentarPago = async (id: number) => {
  const response = await api.post(`api/v1/pagos/${id}/comenzar/`)
  return response.data
}

/* Función para confirmar un pago */
export const confirmarPago = async (id: number) => {
  await api.post(`api/v1/pagos/${id}/confirmar/`)
}

/* Función para cancelar un pago */
export const cancelarIntentoPago = async (id: number) => {
  await api.post(`api/v1/pagos/${id}/cancelar/`)
}

export const cancelarIntentoPagoBeacon = (id: number) => {
  const url = `${import.meta.env.VITE_API_URL}/api/v1/pagos/${id}/cancelar/`

  const data = new Blob([], { type: "application/json" })

  navigator.sendBeacon(url, data)
}