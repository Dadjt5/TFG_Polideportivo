import api from "./api";

/* Funcion para obtener los tipos de actividad, instalacion, reserva, etc. Para el admin */
export const getTipos = async () => {
  const response = await api.get('api/v1/tipos/')
  return response.data
}


/* Función para obtener los pabellones */
export const getPabellones = async () => {
  const response = await api.get('api/v1/pabellones/')
  return response.data;
}

/* Función para obtener los pabellones, pero solo su id y nombre */
export const getPabellonesSimples = async () => {
  const response = await api.get('api/v1/pabellones/simple/')
  return response.data;
}

/* Función para obtener las instalaciones */
export const getInstalaciones = async () => {
  const response = await api.get('api/v1/instalaciones/')
  return response.data;
}

/* Función para obtener las instalaciones, pero solo su id y nombre */
export const getInstalacionesSimples = async () => {
  const response = await api.get('api/v1/instalaciones/simple/')
  return response.data;
}

/* Función para obtener las actividades */
export const getActividades = async () => {
  const response = await api.get('api/v1/actividades/')
  return response.data;
}

/* Función para obtener las actividades, pero solo su id y nombre */
export const getActividadesSimples = async () => {
  const response = await api.get('api/v1/instalaciones/simple/')
  return response.data;
}


/* Función para obtener las tarifas de instalacion */
export const getTarifasInstalacion = async () => {
  const response = await api.get('api/v1/tarifasInstalacion/')
  return response.data;
}


/* Función para obtener los monitores*/
export const getMonitores = async () => {
  const response = await api.get('api/v1/monitores/')
  return response.data;
}


/* Función para obtener los horarios */
export const getHorarios = async () => {
  const response = await api.get('api/v1/horarios/')
  return response.data;
}
