import api from "./api";

/* Función para obtener la informacion de una actividad */
export const getActividadDetalle = async (id) => {
  const response = await api.get(`/api/v1/actividades/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de una actividad */
export const modificarActividad = async (id, data) => {
  const response = await api.patch(`api/v1/actividades/${id}/`, data)
  return response.data
}

/* Función para eliminar una actividad */
export const eliminarActividad = async (id) => {
  const response = await api.delete(`api/v1/actividades/${id}/`)
  return response.data
}

/* Función para obtener la informacion de una instalacion */
export const getInstalacionDetalle = async (id) => {
  const response = await api.get(`/api/v1/instalaciones/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de una instalacion */
export const modificarInstalacion = async (id, data) => {
  const response = await api.patch(`api/v1/instalaciones/${id}/`, data)
  return response.data
}

/* Función para eliminar una instalacion */
export const eliminarInstalacion = async (id) => {
  const response = await api.delete(`api/v1/instalaciones/${id}/`)
  return response.data
}

/* Función para obtener la informacion de un pabellon */
export const getPabellon = async (id) => {
  const response = await api.get(`/api/v1/pabellones/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de un pabellón */
export const modificarPabellon = async (id, data) => {
  const response = await api.patch(`api/v1/pabellones/${id}/`, data)
  return response.data
}

/* Función para eliminar un pabellón */
export const eliminarPabellon = async (id) => {
  const response = await api.delete(`api/v1/pabellones/${id}/`)
  return response.data
}

/* Función para obtener la informacion de instalaciones y actividades indicadas */
export const getActividadesInstalaciones = async (payload) => {
  const response = await api.post('/api/v1/obtener/favoritas/', payload);
  return response.data
}

/* Función para obtener la informacion de una sesión */
export const getSesionDetalle = async (idActividad, idSesion) => {
  const response = await api.get(`/api/v1/actividades/${idActividad}/sesiones/${idSesion}/`);
  return response.data;
};

/* Función para editar los campos indicados de una sesion */
export const modificarSesion = async (id, data) => {
  const response = await api.patch(`api/v1/sesiones/${id}/`, data)
  return response.data
}

/* Función para eliminar una sesion */
export const eliminarSesion = async (id) => {
  const response = await api.delete(`api/v1/sesiones/${id}/`)
  return response.data
}