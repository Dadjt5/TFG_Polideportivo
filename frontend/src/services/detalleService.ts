import api from "./api";

/* Función para obtener la informacion de una actividad */
export const getActividadDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/actividades/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de una actividad */
export const modificarActividad = async (id: number, actividad: any, sesiones: any, deportes: any): Promise<any> => {
  const response = await api.post(`api/v1/actividades/${id}/editar/`, {"actividad": actividad, "sesiones": sesiones, "deportes": deportes})
  return response.data
}

/* Función para eliminar una actividad */
export const eliminarActividad = async (id: number) => {
  const response = await api.delete(`api/v1/actividades/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de un deporte */
export const modificarDeporte = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/deportes/${id}/`, data);
  return response.data;
};

/* Función para eliminar un deporte */
export const eliminarDeporte = async (id: number) => {
  const response = await api.delete(`api/v1/deportes/${id}/`);
  return response.data;
};

/* Función para obtener la informacion de una instalacion */
export const getInstalacionDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/instalaciones/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de una instalacion */
export const modificarInstalacion = async (id: number, instalacion: any, agendas: any, fechasEspeciales: any): Promise<any> => {
  const response = await api.post(`api/v1/instalaciones/${id}/editar/`, {"instalacion": instalacion, "agendas": agendas, "fechasEspeciales": fechasEspeciales})
  return response.data
}

/* Función para eliminar una instalacion */
export const eliminarInstalacion = async (id: number) => {
  const response = await api.delete(`api/v1/instalaciones/${id}/`);
  return response.data;
};

/* Función para obtener la informacion de un pabellon */
export const getPabellonDetalle = async (id: number) => {
  const response = await api.get(`/api/v1/pabellones/${id}/`);
  return response.data;
};

/* Función para editar los campos indicados de un pabellón */
export const modificarPabellon = async (id: number, data: any) => {
  const response = await api.patch(`api/v1/pabellones/${id}/`, data);
  return response.data;
};

/* Función para eliminar un pabellón */
export const eliminarPabellon = async (id: number) => {
  const response = await api.delete(`api/v1/pabellones/${id}/`);
  return response.data;
};

/* Función para obtener la informacion de instalaciones y actividades indicadas */
export const getActividadesInstalaciones = async (payload: any) => {
  const response = await api.post('/api/v1/obtener/favoritas/', payload);
  return response.data;
};

/* Función para obtener la informacion de una sesión */
export const getSesionDetalle = async (idActividad: string, idSesion: string) => {
  const response = await api.get(`/api/v1/actividades/${idActividad}/sesiones/${idSesion}/`);
  return response.data;
};

/* Función para editar los campos indicados de una sesion */
export const modificarSesion = async (id: string, data: any) => {
  const response = await api.patch(`api/v1/sesiones/${id}/`, data);
  return response.data;
};

/* Función para eliminar una sesion */
export const eliminarSesion = async (id: string) => {
  const response = await api.delete(`api/v1/sesiones/${id}/`);
  return response.data;
};
