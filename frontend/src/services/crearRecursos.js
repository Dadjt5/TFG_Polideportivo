import api from "./api";

/* Función para crear un nuevo pabellon */
export const nuevoPabellon = async (payload) => {
  const response = await api.post("api/v1/pabellones/", payload);
  return response.data;
};

/* Función para crear una instalacion */
export const nuevaInstalacion = async (payload) => {
  const response = await api.post("api/v1/instalaciones/", payload);
  return response.data;
};

/* Función para crear una actividad */
export const nuevaActividad = async (payload) => {
  const response = await api.post("api/v1/actividades/", payload);
  return response.data;
};

/* Función para crear una sesion */
export const nuevaSesion = async (payload) => {
  const response = await api.post("api/v1/sesiones/", payload);
  return response.data;
};