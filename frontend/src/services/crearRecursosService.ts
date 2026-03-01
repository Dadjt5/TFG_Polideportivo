import api from "./api"

/* Tipo genérico para payloads */
type Payload = Record<string, any>

/* Función para crear una nueva notificación */
export const nuevaNotificacion = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/notificaciones/nueva/", payload)
  return response.data
}

/* Función para crear un nuevo deporte */
export const nuevoDeporte = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/deportes/", payload)
  return response.data
}

/* Función para crear un nuevo pabellon */
export const nuevoPabellon = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/pabellones/", payload)
  return response.data
}

/* Función para crear una instalacion */
export const nuevaInstalacion = async (instalacion: any, agenda: any, fechasEspeciales: any): Promise<any> => {
  const response = await api.post("api/v1/instalaciones/crear/", {"instalacion": instalacion, "agenda": agenda, "fechasEspeciales": fechasEspeciales})
  return response.data
}

/* Función para crear una actividad */
export const nuevaActividad = async (actividad: any, sesiones: any, deportes: any): Promise<any> => {
  const response = await api.post("api/v1/actividades/crear/", {"actividad": actividad, "sesiones": sesiones, "deportes": deportes})
  return response.data
}

/* Función para crear una sesion */
export const nuevaSesion = async (id: number, payload: Payload): Promise<any> => {
  const response = await api.post(`api/v1/actividades/${id}/sesion/`, payload)
  return response.data
}

/* Función para crear una tarifa de una instalacion */
export const nuevaTarifaInstalacion = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/tarifasInstalacion/", payload)
  return response.data
}

/* Función para crear una tarifa TDA */
export const nuevaTarifaTDA = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/tarifasTDA/", payload)
  return response.data
}

/* Función para crear una tarifa de actividad comun */
export const nuevaTarifaActividadComun = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/actividadesComunes/", payload)
  return response.data
}

/* Función para crear una tarifa de grupo reducido */
export const nuevaTarifaGrupoReducido = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/gruposReducidos/", payload)
  return response.data
}

/* Función para crear una tarifa de fisioterapia */
export const nuevaTarifaFisioterapia = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/fisioterapias/", payload)
  return response.data
}

/* Función para crear un nuevo abono deportivo */
export const nuevoAbonoDeportivo = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/abonosDeportivos/", payload)
  return response.data
}

/* Función para crear un nuevo abono de verano */
export const nuevoAbonoVerano = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/abonosVerano/", payload)
  return response.data
}

/* Función para crear un nuevo abono deportivo */
export const nuevoBono = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/bonos/", payload)
  return response.data
}
