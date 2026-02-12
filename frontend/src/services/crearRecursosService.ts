import api from "./api"

/* Tipo genérico para payloads */
type Payload = Record<string, any>

/* Función para crear un nuevo pabellon */
export const nuevoPabellon = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/pabellones/", payload)
  return response.data
}

/* Función para crear una instalacion */
export const nuevaInstalacion = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/instalaciones/", payload)
  return response.data
}

/* Función para crear una actividad */
export const nuevaActividad = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/actividades/", payload)
  return response.data
}

/* Función para crear una sesion */
export const nuevaSesion = async (payload: Payload): Promise<any> => {
  const response = await api.post("api/v1/sesiones/", payload)
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
